#!/usr/bin/env python3
"""Emit a native editable PPTX companion from a canonical SVG or static HTML visual.

The diagram provider remains responsible for the visual source. This adapter only
normalizes the small SVG feature subset that PPT Master needs, runs its quality
and native-export gates, and writes an auditable companion report.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile


SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)


class WorkflowError(RuntimeError):
    """A user-actionable workflow failure."""


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def trim_output(value: str, limit: int = 4000) -> str:
    value = value.strip()
    return value if len(value) <= limit else value[-limit:]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_declarations(body: str) -> dict[str, str]:
    declarations: dict[str, str] = {}
    for item in body.split(";"):
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            declarations[key] = value
    return declarations


def read_class_rules(root: ET.Element) -> dict[str, dict[str, str]]:
    rules: dict[str, dict[str, str]] = {}
    for element in root.iter():
        if local_name(element.tag) != "style":
            continue
        css = "".join(element.itertext())
        for selector_text, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            declarations = parse_declarations(body)
            for selector in selector_text.split(","):
                selector = selector.strip()
                if selector.startswith(".") and re.fullmatch(r"\.[A-Za-z0-9_-]+", selector):
                    rules.setdefault(selector[1:], {}).update(declarations)
    return rules


def extract_svg_fragment(document: str) -> str:
    """Extract the first balanced SVG element from a static HTML document."""

    token_pattern = re.compile(r"<\s*(/?)\s*svg\b[^>]*>", re.IGNORECASE)
    start_match = None
    depth = 0
    for match in token_pattern.finditer(document):
        closing = bool(match.group(1))
        if not closing and start_match is None:
            start_match = match
            depth = 1
            continue
        if start_match is None:
            continue
        if closing:
            depth -= 1
            if depth == 0:
                return document[start_match.start() : match.end()]
        elif match.group(0).rstrip().endswith("/>"):
            continue
        else:
            depth += 1
    raise WorkflowError("HTML source does not contain a complete <svg>...</svg> element")


def load_svg_source(source: Path) -> tuple[str, str, list[str]]:
    if not source.exists():
        raise WorkflowError(f"source file not found: {source}")
    if source.suffix.lower() in {".html", ".htm"}:
        fragment = extract_svg_fragment(source.read_text(encoding="utf-8"))
        fragment = html_lib.unescape(fragment)
        source_kind = "static-html-svg-extraction"
        warnings = [
            "HTML input was reduced to its first static SVG; dynamic controls and non-SVG HTML are not represented in PPTX."
        ]
    else:
        fragment = source.read_text(encoding="utf-8")
        source_kind = "svg"
        warnings = []

    try:
        root = ET.fromstring(fragment)
    except ET.ParseError as exc:
        raise WorkflowError(f"source is not valid XML/SVG: {exc}") from exc
    if local_name(root.tag) != "svg":
        raise WorkflowError(f"source root is <{local_name(root.tag)}>; expected <svg>")
    return fragment, source_kind, warnings


def color_key(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", "", value.strip().lower())


def marker_reference(value: str | None) -> str | None:
    if not value:
        return None
    match = re.fullmatch(r"url\(#([^)]+)\)", value.strip())
    return match.group(1) if match else None


def marker_fill(marker: ET.Element) -> str | None:
    for key in ("fill", "color"):
        if marker.get(key):
            return marker.get(key)
    for child in marker.iter():
        if child is marker:
            continue
        if child.get("fill") and child.get("fill") != "none":
            return child.get("fill")
    return None


def prepare_svg(fragment: str, output_path: Path) -> dict[str, Any]:
    root = ET.fromstring(fragment)
    parent_map = {child: parent for parent in root.iter() for child in parent}
    rules = read_class_rules(root)
    removed_nodes: list[str] = []
    inlined_classes = 0
    inlined_style_attributes = 0
    removed_filter_attributes = 0
    generated_markers = 0

    for element in list(root.iter()):
        tag = local_name(element.tag)
        if tag in {"style", "filter"}:
            parent = parent_map.get(element)
            if parent is not None:
                parent.remove(element)
                removed_nodes.append(tag)
            continue

        class_names = element.get("class", "").split()
        for class_name in class_names:
            declarations = rules.get(class_name, {})
            if declarations:
                inlined_classes += 1
            for key, value in declarations.items():
                element.attrib.setdefault(key, value)
        element.attrib.pop("class", None)

        inline = element.get("style")
        if inline:
            inlined_style_attributes += 1
            for key, value in parse_declarations(inline).items():
                element.attrib.setdefault(key, value)
            element.attrib.pop("style", None)

        if element.attrib.pop("filter", None) is not None:
            removed_filter_attributes += 1

    defs = next((element for element in root if local_name(element.tag) == "defs"), None)
    if defs is None:
        defs = ET.Element(f"{{{SVG_NS}}}defs")
        root.insert(0, defs)

    marker_nodes: dict[str, ET.Element] = {}
    marker_by_color: dict[str, str] = {}
    for element in defs:
        if local_name(element.tag) != "marker" or not element.get("id"):
            continue
        marker_id = element.get("id")
        marker_nodes[marker_id] = element
        fill = marker_fill(element)
        if fill:
            marker_by_color[color_key(fill)] = marker_id

    for element in root.iter():
        stroke = element.get("stroke")
        if not stroke:
            continue
        stroke_key = color_key(stroke)
        for attribute in ("marker-start", "marker-end"):
            original = marker_reference(element.get(attribute))
            if not original:
                continue
            target_id = marker_by_color.get(stroke_key)
            if target_id is None and original in marker_nodes:
                clone = copy.deepcopy(marker_nodes[original])
                target_id = f"lvsea-draw-arrow-{len(marker_nodes) + generated_markers + 1}"
                clone.set("id", target_id)
                for child in clone.iter():
                    if local_name(child.tag) in {"path", "polygon", "polyline"}:
                        if child.get("fill") and child.get("fill") != "none":
                            child.set("fill", stroke)
                defs.append(clone)
                marker_by_color[stroke_key] = target_id
                marker_nodes[target_id] = clone
                generated_markers += 1
            if target_id:
                element.set(attribute, f"url(#{target_id})")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    ET.parse(output_path)
    return {
        "removed_css_filter_nodes": len(removed_nodes),
        "inlined_class_assignments": inlined_classes,
        "inlined_style_attributes": inlined_style_attributes,
        "removed_filter_attributes": removed_filter_attributes,
        "generated_arrow_markers": generated_markers,
    }


def discover_ppt_master(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    for env_name in ("PPT_MASTER_SKILL_DIR", "PPT_MASTER_DIR"):
        if os.environ.get(env_name):
            candidates.append(Path(os.environ[env_name]).expanduser())
    home = Path.home()
    candidates.extend(
        [
            home / ".codex" / "skills" / "ppt-master",
            home / ".agents" / "skills" / "ppt-master",
        ]
    )
    for candidate in candidates:
        if (candidate / "scripts" / "svg_to_pptx.py").is_file() and (
            candidate / "scripts" / "svg_quality_checker.py"
        ).is_file():
            return candidate.resolve()
    rendered = ", ".join(str(path) for path in candidates)
    raise WorkflowError(
        "PPT Master was not discovered. Install it or set PPT_MASTER_SKILL_DIR. "
        f"Checked: {rendered}"
    )


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return {
        "command": [str(part) for part in command],
        "returncode": result.returncode,
        "stdout": trim_output(result.stdout),
        "stderr": trim_output(result.stderr),
    }


def write_spec_lock(project_dir: Path, root: ET.Element, title: str, output_format: str) -> Path:
    view_box = root.get("viewBox", "").strip()
    if not view_box:
        raise WorkflowError("SVG root must declare viewBox for a stable PPTX canvas")
    fills: list[str] = []
    fonts: list[str] = []
    sizes: list[int] = []
    for element in root.iter():
        for attribute in ("fill", "stroke"):
            value = element.get(attribute)
            if value and value.startswith("#") and value.upper() not in fills:
                fills.append(value.upper())
        family = element.get("font-family")
        if family and family not in fonts:
            fonts.append(family)
        size = element.get("font-size", "").strip().lower().removesuffix("px")
        try:
            numeric_size = int(float(size))
        except ValueError:
            numeric_size = 0
        if numeric_size > 0 and numeric_size not in sizes:
            sizes.append(numeric_size)
    sizes.sort()
    body_size = 16 if 16 in sizes else (sizes[0] if sizes else 16)
    title_size = max(sizes) if sizes else 28
    spec = [
        "<!-- ppt-master-schema: spec-lock/v1 -->",
        "# Execution Lock",
        "",
        "## canvas",
        f"- viewBox: {view_box}",
        f"- format: {output_format}",
        "",
        "## communication",
        "- objective: preserve the source visual as an editable PPTX companion",
        f"- source_title: {title or 'untitled visual'}",
        "- consumption_mode: presentation",
        "",
        "## mode",
        "- mode: custom",
        "",
        "## visual_style",
        "- visual_style: source-faithful scientific or technical visual",
        "",
        "## colors",
        f"- bg: {fills[0] if fills else '#FFFFFF'}",
        f"- primary: {fills[1] if len(fills) > 1 else (fills[0] if fills else '#404040')}",
        f"- accent: {fills[2] if len(fills) > 2 else (fills[1] if len(fills) > 1 else '#B12317')}",
        f"- text: {fills[3] if len(fills) > 3 else '#404040'}",
        *[f"- source_color_{index:02d}: {value}" for index, value in enumerate(fills[4:16], start=1)],
        "",
        "## typography",
        f"- font_family: {', '.join(fonts[:8]) or 'Microsoft YaHei, Arial, sans-serif'}",
        f"- body: {body_size}",
        f"- title: {title_size}",
        *[f"- size_{value}: {value}" for value in sizes],
        "",
        "## pptx_structure",
        "- mode: flat",
        "",
        "## forbidden",
        "- script-driven HTML state, foreignObject, and unsupported CSS effects",
        "- silent omission of a required companion when SVG/HTML conversion fails",
        "",
    ]
    path = project_dir / "spec_lock.md"
    path.write_text("\n".join(spec), encoding="utf-8")
    return path


def inspect_pptx(path: Path) -> dict[str, Any]:
    namespaces = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
    slide_names: list[str] = []
    with ZipFile(path) as archive:
        members = archive.namelist()
        slide_names = sorted(
            name
            for name in members
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
        shapes = 0
        graphic_frames = 0
        pictures = 0
        text_runs = 0
        for slide_name in slide_names:
            root = ET.fromstring(archive.read(slide_name))
            shapes += len(root.findall(".//p:sp", namespaces))
            graphic_frames += len(root.findall(".//p:graphicFrame", namespaces))
            pictures += len(root.findall(".//p:pic", namespaces))
            text_runs += len(root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
        media = [name for name in members if name.startswith("ppt/media/")]
    return {
        "bytes": path.stat().st_size,
        "slides": len(slide_names),
        "native_shape_objects": shapes,
        "graphic_frames": graphic_frames,
        "picture_objects": pictures,
        "media_members": len(media),
        "text_runs": text_runs,
        "zip_integrity": "passed",
    }


def find_executable(names: list[str]) -> str | None:
    is_pdftoppm = any(name.lower().startswith("pdftoppm") for name in names)
    if is_pdftoppm:
        runtime_root = Path.home() / ".cache" / "codex-runtimes"
        if runtime_root.is_dir():
            for candidate in runtime_root.rglob("pdftoppm.exe"):
                return str(candidate)
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    candidates = [
        Path("C:/Program Files/LibreOffice/program/soffice.exe"),
        Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe"),
    ]
    if any(name.lower().startswith("soffice") for name in names):
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
    return None


def render_preview(pptx_path: Path, preview_path: Path, work_dir: Path) -> dict[str, Any]:
    soffice = os.environ.get("SOFFICE") or find_executable(["soffice", "soffice.exe"])
    pdftoppm = os.environ.get("PDFTOPPM") or find_executable(["pdftoppm", "pdftoppm.exe"])
    if not soffice or not pdftoppm:
        return {
            "status": "skipped",
            "reason": "LibreOffice soffice or Poppler pdftoppm was not discovered",
        }
    render_dir = work_dir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)
    profile_dir = render_dir / "lo-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = render_dir / f"{pptx_path.stem}.pdf"
    convert = run_command(
        [
            soffice,
            "--headless",
            f"-env:UserInstallation=file:///{profile_dir.as_posix()}",
            "--convert-to",
            "pdf",
            "--outdir",
            str(render_dir),
            str(pptx_path),
        ],
        cwd=render_dir,
    )
    if convert["returncode"] != 0 or not pdf_path.is_file():
        return {"status": "blocked", "stage": "libreoffice", "result": convert}
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = preview_path.with_suffix("")
    raster = run_command(
        [pdftoppm, "-png", "-f", "1", "-singlefile", str(pdf_path), str(prefix)],
        cwd=render_dir,
    )
    if raster["returncode"] != 0 or not preview_path.is_file():
        return {"status": "blocked", "stage": "pdftoppm", "result": raster}
    return {
        "status": "passed",
        "preview": str(preview_path.resolve()),
        "pdf": str(pdf_path.resolve()),
        "libreoffice": convert,
        "pdftoppm": raster,
    }


def make_report_path(output: Path, explicit: str | None) -> Path:
    return Path(explicit).expanduser().resolve() if explicit else output.with_suffix(".report.json")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    report_path = make_report_path(output, args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() != ".pptx":
        raise WorkflowError("output must use the .pptx extension")

    fragment, source_kind, source_warnings = load_svg_source(source)
    source_root = ET.fromstring(fragment)
    view_box = source_root.get("viewBox", "").split()
    if len(view_box) != 4:
        raise WorkflowError("SVG root must declare a four-value viewBox")
    try:
        canvas_width = float(view_box[2])
        canvas_height = float(view_box[3])
    except ValueError as exc:
        raise WorkflowError(f"invalid SVG viewBox: {source_root.get('viewBox')}") from exc
    if canvas_width <= 0 or canvas_height <= 0:
        raise WorkflowError("SVG viewBox width and height must be positive")
    if args.format == "ppt169" and abs((canvas_width / canvas_height) - (16 / 9)) > 0.03:
        raise WorkflowError(
            f"source canvas {canvas_width:g}x{canvas_height:g} is not 16:9; use --format for another registered canvas"
        )

    ppt_master = discover_ppt_master(args.ppt_master_dir)
    work_parent = Path(args.work_dir).expanduser().resolve() if args.work_dir else None
    if work_parent:
        work_parent.mkdir(parents=True, exist_ok=True)
    temporary_parent = str(work_parent) if work_parent else None
    project_dir = Path(tempfile.mkdtemp(prefix="lvsea-draw-pptx-", dir=temporary_parent))
    preserve_project = work_parent is not None
    svg_output = project_dir / "svg_output"
    svg_output.mkdir(parents=True, exist_ok=True)
    validation_dir = project_dir / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)

    normalized_svg = svg_output / "slide_01.svg"
    normalization = prepare_svg(fragment, normalized_svg)
    normalized_root = ET.parse(normalized_svg).getroot()
    title_element = next((element for element in normalized_root if local_name(element.tag) == "title"), None)
    title = "".join(title_element.itertext()).strip() if title_element is not None else ""
    spec_lock = write_spec_lock(project_dir, normalized_root, title, args.format)

    quality_report_path = validation_dir / "svg-quality.json"
    quality = run_command(
        [
            sys.executable,
            str(ppt_master / "scripts" / "svg_quality_checker.py"),
            str(project_dir),
            "--format",
            args.format,
            "--stage",
            "final",
            "--json",
            "--json-output",
            str(quality_report_path),
        ],
        cwd=ppt_master,
    )
    quality_data: dict[str, Any] = {}
    if quality_report_path.is_file():
        quality_data = json.loads(quality_report_path.read_text(encoding="utf-8"))
    quality_summary = quality_data.get("summary", {})
    quality_status = "blocked" if quality["returncode"] != 0 else (
        "passed-with-warnings" if quality_summary.get("warnings", 0) else "passed"
    )
    if quality["returncode"] != 0:
        raise WorkflowError(f"PPT Master SVG quality gate failed: {quality.get('stderr') or quality.get('stdout')}")

    export_path = project_dir / "exports" / f"{output.stem}.pptx"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export = run_command(
        [
            sys.executable,
            str(ppt_master / "scripts" / "svg_to_pptx.py"),
            str(project_dir),
            "-o",
            str(export_path),
            "-f",
            args.format,
            "--pptx-structure",
            "flat",
            "--conversion-trace",
            "--no-notes",
            "-t",
            "none",
        ],
        cwd=ppt_master,
    )
    if export["returncode"] != 0 or not export_path.is_file():
        raise WorkflowError(f"PPT Master native export failed: {export.get('stderr') or export.get('stdout')}")

    shutil.copy2(export_path, output)
    copied_quality = output.with_name(f"{output.stem}-svg-quality.json")
    shutil.copy2(quality_report_path, copied_quality)
    trace_source = Path(f"{export_path}.trace.json")
    copied_trace: Path | None = None
    if trace_source.is_file():
        copied_trace = output.with_name(f"{output.stem}.trace.json")
        shutil.copy2(trace_source, copied_trace)

    package = inspect_pptx(output)
    preview: dict[str, Any] = {"status": "not-requested"}
    preview_path: Path | None = None
    if args.render_preview:
        preview_path = (
            Path(args.preview_output).expanduser().resolve()
            if args.preview_output
            else output.with_name(f"{output.stem}-preview.png")
        )
        preview = render_preview(output, preview_path, project_dir)

    warnings = list(source_warnings)
    if source.suffix.lower() in {".html", ".htm"}:
        warnings.append("Only the first static SVG was converted; HTML interaction and animation are not editable PPTX objects.")
    if package["picture_objects"] or package["media_members"]:
        warnings.append("Embedded image objects remain pictures; text and supported SVG geometry are the editable native portion.")
    if preview.get("status") in {"skipped", "not-requested"}:
        warnings.append("Visual preview was not produced by this invocation; perform a browser/LibreOffice readback for release delivery.")
    if quality_status == "passed-with-warnings":
        warnings.append(f"PPT Master SVG quality reported {quality_summary.get('warnings', 0)} advisory warning(s); no blocking errors.")
    if preview.get("status") == "blocked":
        warnings.append("PPTX export passed, but the optional visual preview command failed.")

    report: dict[str, Any] = {
        "schema": "lvsea-draw.editable-pptx-report.v1",
        "status": "passed-with-warnings" if warnings else "passed",
        "input": {
            "source": str(source),
            "source_sha256": sha256_file(source),
            "source_kind": source_kind,
            "title": title,
            "viewBox": source_root.get("viewBox"),
        },
        "adapter": {
            "ppt_master_dir": str(ppt_master),
            "project_dir": str(project_dir) if preserve_project else None,
            "project_lifecycle": "preserved" if preserve_project else "temporary; removed after export",
            "format": args.format,
            "normalization": normalization,
            "spec_lock": str(spec_lock),
        },
        "validation": {
            "svg_quality": {
                "status": quality_status,
                "command": quality,
                "summary": quality_summary,
                "report": str(copied_quality),
            },
            "native_export": export,
            "pptx_package": package,
            "visual_preview": preview,
        },
        "outputs": {
            "pptx": str(output),
            "svg_quality_report": str(copied_quality),
            "conversion_trace": str(copied_trace) if copied_trace else None,
            "preview": str(preview_path) if preview.get("status") == "passed" and preview_path else None,
            "report": str(report_path),
        },
        "warnings": warnings,
        "limitations": [
            "PPT Master creates native DrawingML objects for supported SVG text and geometry; unsupported or embedded image content is not converted into editable text/shapes.",
            "A dynamic HTML application must first emit a canonical static SVG if it needs a PPTX companion.",
        ],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not preserve_project:
        shutil.rmtree(project_dir, ignore_errors=True)
    return report


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Create a native editable PPTX companion from SVG or static HTML.")
    parser.add_argument("source", help="Canonical SVG or self-contained/static HTML containing an SVG")
    parser.add_argument("-o", "--output", required=True, help="Output .pptx path")
    parser.add_argument("--report", help="JSON report path; defaults to the PPTX stem with .report.json")
    parser.add_argument("--ppt-master-dir", help="PPT Master skill directory; otherwise discover local installs")
    parser.add_argument("--work-dir", help="Parent directory for a preserved temporary PPT Master project")
    parser.add_argument("--format", choices=["ppt169", "ppt43", "wechat", "xiaohongshu", "moments", "story", "banner", "a4"], default="ppt169")
    parser.add_argument("--render-preview", action="store_true", help="Best-effort LibreOffice + Poppler first-slide preview")
    parser.add_argument("--preview-output", help="Preview PNG path when --render-preview is used")
    args = parser.parse_args()

    try:
        report = execute(args)
    except (OSError, ValueError, WorkflowError, ET.ParseError, json.JSONDecodeError) as exc:
        output = Path(args.output).expanduser().resolve()
        report_path = make_report_path(output, args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        failure = {
            "schema": "lvsea-draw.editable-pptx-report.v1",
            "status": "blocked",
            "error": str(exc),
            "outputs": {"pptx": str(output), "report": str(report_path)},
        }
        report_path.write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
