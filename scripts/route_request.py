#!/usr/bin/env python3
"""Route a diagram request to the smallest reliable lvsea-draw workflow."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "codebase-knowledge-graph": {
        "executor": "understand",
        "patterns": [
            (r"知识图谱|代码.*(理解|关系|依赖)|理解.*(仓库|代码库|项目)|变更影响|入职导览|业务域|代码库", 5),
            (r"github\.com|repo|repository|仓库|monorepo", 1),
        ],
        "outputs": ["knowledge-graph.json", "interactive dashboard", "analysis notes"],
        "validation": ["graph directory and graph commit freshness", "project-scoped git diff"],
        "fallback": ["evidence-architecture", "technical-explainer-illustrator"],
    },
    "editable-drawio": {
        "executor": "drawio-skill",
        "patterns": [
            (r"draw\.?io|\.drawio|drawio-skill|agents365|xml|云厂商图标|实时.*(编辑|预览)", 6),
            (r"可编辑|继续修改|导出.*(png|svg)", 1),
        ],
        "outputs": [".drawio or XML source", "optional PNG/SVG"],
        "validation": [
            "XML parse and cell/edge reference checks",
            "draw.io CLI/version probe when import or export is requested",
            "self-check or PNG visual readback when the provider supports it",
        ],
        "fallback": ["bruce-drawio", "precise-technical-graphic", "evidence-architecture"],
        "provider_policy": "Prefer the installed drawio-skill; use bruce-drawio or Draw.io MCP only when actually detected.",
    },
    "whiteboard-workbench": {
        "executor": "drawnix",
        "patterns": [
            (r"白板|思维导图|自由画|草图|先.*(讨论|梳理).*结构|mermaid.*(转|变).*流程图", 6),
            (r"可编辑|手工调整|无限画布", 2),
        ],
        "outputs": [".drawnix or JSON export", "PNG preview"],
        "validation": ["service and port probe", "exported file exists and is readable"],
        "fallback": ["handdrawn-argument", "editable-drawio"],
    },
    "handdrawn-argument": {
        "executor": "excalidraw-diagram",
        "patterns": [
            (r"excalidraw|手绘|手账|涂鸦|草图风|视觉论证|一图.*讲清", 5),
            (r"概念教学|证据卡片|故事化", 2),
        ],
        "outputs": [".excalidraw JSON", "rendered PNG/SVG"],
        "validation": ["JSON bindings", "render-view-fix loop", "visual review"],
        "fallback": ["whiteboard-workbench", "interactive-widget"],
    },
    "precise-technical-graphic": {
        "executor": "fireworks-tech-graph",
        "patterns": [
            (r"生成\s*gif|制作\s*gif|动画.*svg|让.*(图|svg).*动|gif", 7),
            (r"uml|er\s*(图|diagram)?|c4|svg|png|几何|geometry|云部署|事件流|可靠性|技术图", 4),
            (r"架构图|流程图|时序图|数据流图|状态机", 1),
        ],
        "outputs": ["SVG source", "PNG render", "optional GIF and motion report", "offline HTML"],
        "validation": ["SVG/XML/marker/geometry checks", "PNG visual readback"],
        "fallback": ["evidence-architecture", "interactive-widget"],
    },
    "explainer-image-set": {
        "executor": "technical-explainer-illustrator",
        "patterns": [
            (r"技术解读|技术解释图|一图看懂|仓库.*(配图|图组)|论文.*(图|配图)|技术报告.*(图|配图)", 6),
            (r"16\s*[:：]\s*9|成套|图组|事实台账|prompt.*包|提示词包", 3),
        ],
        "outputs": ["SOURCE-MANIFEST", "CLAIM-LEDGER", "VISUAL-PLAN", "image set", "QA"],
        "validation": ["source locations", "per-image route", "image and text QA"],
        "fallback": ["evidence-architecture", "precise-technical-graphic"],
    },
    "infographic-composition": {
        "executor": "antv-infographic",
        "patterns": [
            (r"信息图|信息可视化|数据故事|数据叙事|信息长图|图解海报|列表信息图|对比信息图|时间线信息图|金字塔信息图|漏斗信息图|infographic|antv\s*infographic", 7),
            (r"时间线|漏斗|金字塔|对比.*图|列表.*图", 5),
            (r"声明式.*(图|可视化)|infographic\s*(syntax|dsl)|信息图.*(html|svg|png)|编辑.*信息图", 2),
        ],
        "outputs": ["Infographic syntax source", "standalone HTML/SVG", "optional PNG"],
        "validation": [
            "template and syntax parse",
            "single compatible data family with language and icon checks",
            "browser/SVG viewBox, text-fit, and visual readback",
        ],
        "fallback": ["editorial-diagram", "precise-technical-graphic", "interactive-widget"],
        "provider_policy": "Prefer @antv/infographic or an installed AntV Infographic skill; otherwise fall back without claiming AntV rendering.",
    },
    "interactive-widget": {
        "executor": "generative-ui-mcp",
        "patterns": [
            (r"交互式|widget|组件|dashboard|图表|chart|计算器|滑块|数据可视化|矩阵|时间线", 5),
            (r"html|svg|可嵌入|show-widget", 2),
        ],
        "outputs": ["single HTML/SVG widget", "optional Chart.js chart"],
        "validation": ["viewBox and text fit", "controls change the view", "local resource readback"],
        "fallback": ["animated-explainer-html", "precise-technical-graphic"],
    },
    "animated-explainer-html": {
        "executor": "science-content-ppt",
        "patterns": [
            (r"动画网页|演示网页|仿\s*ppt|轮播|录屏|科普.*(演示|可视化)|流程.*动画|动效", 5),
            (r"html|单文件|播放|缓入", 2),
        ],
        "outputs": ["single HTML presentation", "optional screenshots or video source"],
        "validation": ["browser render", "animation reset/replay", "responsive and safe area"],
        "fallback": ["interactive-widget", "evidence-architecture"],
    },
    "editorial-document": {
        "executor": "kami-or-local-document-skill",
        "patterns": [
            (r"一页纸|白皮书|报告.*(排版|图解)|ppt|slides|演示文稿|文档内嵌|落地页|作品集", 5),
            (r"图解|单页|版式|排版", 2),
        ],
        "outputs": ["HTML/PDF/PPT/Slides with embedded diagram"],
        "validation": ["page and font capacity", "rendered preview", "source fact readback"],
        "fallback": ["evidence-architecture", "interactive-widget"],
    },
    "editorial-diagram": {
        "executor": "diagram-design",
        "patterns": [
            (r"diagram\s*design|editorial\s*diagram|品牌.*(图|配色)|品牌化.*(图|视觉)|样式指南|style\s*guide|重绘.*(mermaid|draw\.?io)|mermaid.*重绘|draw\.?io.*重绘", 6),
            (r"泳道|时间线|象限|金字塔|漏斗|树状图|组织结构|venn|swot|循环|飞轮|矩阵|雷达图|分层.*图", 3),
        ],
        "outputs": ["self-contained HTML", "accessible SVG", "optional PNG and style receipt"],
        "validation": [
            "semantic pattern and density check",
            "brand/style-guide decision recorded",
            "accessible SVG title/description and text-fit checks",
            "browser or image visual readback",
        ],
        "fallback": ["infographic-composition", "precise-technical-graphic", "editorial-document"],
        "provider_policy": "Prefer diagram-design for static branded diagrams; do not silently ship its default skin into an identified brand project.",
    },
    "custom-graph-application": {
        "executor": "antv-x6-engineering",
        "patterns": [
            (r"\bx6\b|图编辑器|业务拓扑.*(应用|系统)|节点.*边.*端口|react.*vue.*(图|画布)|web.*(图|编辑)", 6),
            (r"可交互.*(编辑|拖拽)|插件|事件系统|服务端渲染", 2),
        ],
        "outputs": ["editable web application source", "tests", "export sample"],
        "validation": ["build/type checks", "browser interaction", "export/readback"],
        "fallback": ["editable-drawio", "whiteboard-workbench"],
    },
    "preview-and-qa": {
        "executor": "svg-preview-or-local-browser",
        "patterns": [
            (r"预览|打开.*svg|检查.*svg|核对.*裁切|浏览器显示|显示不对|黑色背景", 6),
            (r"inspect|preview|render.*check", 2),
        ],
        "outputs": ["preview result", "optional fixed copy"],
        "validation": ["XML parse", "browser/Inkscape visual inspection"],
        "fallback": ["precise-technical-graphic"],
    },
    "evidence-architecture": {
        "executor": "archify",
        "patterns": [
            (r"架构|流程|时序|数据流|生命周期|状态机|审批|ci\s*/?\s*cd|调用链|数据血缘|系统图", 4),
            (r"仓库|代码库|系统|服务|接口|缓存|数据库|消息队列", 2),
        ],
        "outputs": ["Typed JSON IR", "standalone HTML", "optional PNG/SVG/WebM/share card"],
        "validation": ["schema/layout/route/label clearance checks", "HTML/SVG readback"],
        "fallback": ["precise-technical-graphic", "interactive-widget"],
    },
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def score_routes(text: str) -> list[tuple[str, float, list[str]]]:
    normalized = normalize(text)
    scored: list[tuple[str, float, list[str]]] = []
    for route_id, route in ROUTES.items():
        score = 0.0
        reasons: list[str] = []
        for pattern, weight in route["patterns"]:
            if re.search(pattern, normalized, flags=re.IGNORECASE):
                score += weight
                reasons.append(pattern)
        if score:
            scored.append((route_id, score, reasons))
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored


def secondary_routes(text: str, primary: str) -> list[str]:
    normalized = normalize(text)
    candidates: list[str] = []
    if primary == "evidence-architecture" and re.search(r"信息图|infographic|数据故事|数据叙事", normalized):
        candidates.append("infographic-composition")
    if primary == "infographic-composition" and re.search(r"品牌|style\s*guide|mermaid|draw\.?io|重绘", normalized):
        candidates.append("editorial-diagram")
    if primary == "infographic-composition" and re.search(r"交互|dashboard|widget|动画|播放", normalized):
        candidates.append("interactive-widget")
    if primary == "infographic-composition" and re.search(r"ppt|slides|报告|一页纸|白皮书", normalized):
        candidates.append("editorial-document")
    if primary == "editorial-diagram" and re.search(r"ppt|slides|报告|一页纸|白皮书", normalized):
        candidates.append("editorial-document")
    if primary == "codebase-knowledge-graph" and re.search(r"架构|流程|地图|可视化", normalized):
        candidates.append("evidence-architecture")
    if primary == "evidence-architecture" and re.search(r"svg|png|gif|uml|er|几何", normalized):
        candidates.append("precise-technical-graphic")
    if primary == "evidence-architecture" and re.search(r"ppt|slides|一页纸|报告", normalized):
        candidates.append("editorial-document")
    if primary == "explainer-image-set" and re.search(r"架构|流程|svg|png", normalized):
        candidates.append("precise-technical-graphic")
    if primary == "whiteboard-workbench" and re.search(r"正式|交付|draw\.?io|svg|png", normalized):
        candidates.append("editable-drawio")
    if primary == "interactive-widget" and re.search(r"动画|播放|录屏", normalized):
        candidates.append("animated-explainer-html")
    if primary == "animated-explainer-html" and re.search(r"组件|chart|图表|交互", normalized):
        candidates.append("interactive-widget")
    if primary == "editorial-document" and re.search(r"架构|流程|svg|数据流", normalized):
        candidates.append("evidence-architecture")
    return list(dict.fromkeys(route for route in candidates if route != primary))[:2]


def build_plan(text: str) -> dict[str, Any]:
    normalized = normalize(text)
    scored = score_routes(text)
    if not scored:
        primary = "evidence-architecture"
        score = 0.0
        matched: list[str] = []
    else:
        primary, score, matched = scored[0]

    ambiguous = not scored or score < 4 or (len(scored) > 1 and scored[0][1] - scored[1][1] < 1.5)
    generic_request = bool(re.fullmatch(r"(帮我)?(画个图|做个图|做可视化|画图|可视化)", normalized))
    needs_clarification = generic_request or not scored
    route = ROUTES[primary]

    reasons = [
        f"主路由 {primary} 命中 {len(matched)} 组意图信号",
        "先选择最小充分的执行器，再考虑协作路由",
    ]
    if ambiguous and not needs_clarification:
        reasons.append("存在近邻路由，按明确输出格式和事实风险做最终裁决")
    if needs_clarification:
        reasons.append("请求缺少关系类型或目标格式，不能可靠决定唯一渲染器")

    return {
        "schema_version": "1.0",
        "request": text,
        "route": primary,
        "primary_executor": route["executor"],
        "secondary_routes": secondary_routes(text, primary),
        "confidence": round(min(0.99, 0.35 + score / 14), 2),
        "reasons": reasons,
        "matched_signals": matched,
        "output_contract": route["outputs"],
        "validation": route["validation"],
        "fallback": route["fallback"],
        "provider_policy": route.get("provider_policy"),
        "needs_clarification": needs_clarification,
        "clarification": (
            "请补充：最终要可编辑文件、可直接打开的 HTML，还是图片/PPT？"
            if needs_clarification
            else None
        ),
        "source_evidence_required": primary
        in {
            "codebase-knowledge-graph",
            "evidence-architecture",
            "explainer-image-set",
            "precise-technical-graphic",
            "infographic-composition",
            "editorial-diagram",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a diagram request.")
    parser.add_argument("--text", help="Request text. Reads stdin when omitted.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read()
    if not text.strip():
        parser.error("provide --text or stdin")
    plan = build_plan(text)
    print(json.dumps(plan, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
