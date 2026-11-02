#!/usr/bin/env python3
"""Unit checks for the SVG-to-PPTX companion adapter."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from emit_editable_pptx import extract_svg_fragment, prepare_svg  # noqa: E402


class EditablePptxAdapterTests(unittest.TestCase):
    def test_extracts_first_static_svg_from_html(self) -> None:
        document = "<html><body><svg viewBox='0 0 16 9'><rect width='16' height='9'/></svg></body></html>"
        fragment = extract_svg_fragment(document)
        self.assertIn("viewBox='0 0 16 9'", fragment)
        self.assertEqual(ET.fromstring(fragment).tag.split("}")[-1], "svg")

    def test_inlines_css_removes_filters_and_preserves_arrow(self) -> None:
        fragment = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 90">
          <defs>
            <marker id="arrow" viewBox="0 0 10 10"><path d="M0 0L10 5L0 10z" fill="#123456"/></marker>
            <filter id="shadow"><feDropShadow dx="0" dy="1"/></filter>
            <style>.card { fill: #fff; filter: url(#shadow); } .flow { stroke: #123456; }</style>
          </defs>
          <rect class="card" x="0" y="0" width="100" height="50"/>
          <path class="flow" d="M10 10 H80" marker-end="url(#arrow)"/>
        </svg>
        """
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "slide.svg"
            stats = prepare_svg(fragment, output)
            root = ET.parse(output).getroot()
            serialized = output.read_text(encoding="utf-8")
            self.assertGreater(stats["removed_css_filter_nodes"], 0)
            self.assertNotIn("class=", serialized)
            self.assertNotIn("<filter", serialized)
            self.assertNotIn("filter=", serialized)
            path = next(element for element in root.iter() if element.tag.split("}")[-1] == "path" and element.get("marker-end"))
            self.assertTrue(path.get("marker-end", "").startswith("url(#"))


if __name__ == "__main__":
    unittest.main()
