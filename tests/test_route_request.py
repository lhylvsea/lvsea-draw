#!/usr/bin/env python3
"""Small regression suite for the lvsea-draw router."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from route_request import build_plan  # noqa: E402


class RouteRequestTests(unittest.TestCase):
    def assert_route(self, text: str, expected: str) -> None:
        plan = build_plan(text)
        self.assertEqual(plan["route"], expected, plan)
        self.assertTrue(plan["primary_executor"])
        self.assertTrue(plan["output_contract"])
        self.assertTrue(plan["validation"])
        self.assertTrue(plan["editable_pptx_companion"]["emitter"])

    def test_codebase_graph(self) -> None:
        self.assert_route("分析这个 GitHub 仓库，生成可搜索的代码知识图谱和变更影响", "codebase-knowledge-graph")

    def test_drawio_wins_over_generic_flow(self) -> None:
        self.assert_route("把安全生产异常闭环做成可继续修改的 Draw.io XML", "editable-drawio")

    def test_drawio_skill_provider(self) -> None:
        plan = build_plan("用 Agents365 drawio-skill 把 Terraform 和 SQL 生成可继续修改的多页 drawio")
        self.assertEqual(plan["route"], "editable-drawio", plan)
        self.assertEqual(plan["primary_executor"], "drawio-skill")

    def test_infographic_composition(self) -> None:
        plan = build_plan("把培训要点做成中文信息图和数据故事，保留 Infographic DSL 并导出 SVG")
        self.assertEqual(plan["route"], "infographic-composition", plan)
        self.assertIn("Infographic syntax source", plan["output_contract"])
        self.assertIn("editorial-diagram", plan["fallback"])

    def test_editorial_diagram(self) -> None:
        plan = build_plan("按品牌规范把 Mermaid 重绘成自包含 HTML 和可访问 SVG")
        self.assertEqual(plan["route"], "editorial-diagram", plan)
        self.assertEqual(plan["primary_executor"], "diagram-design")
        self.assertTrue(plan["provider_policy"])

    def test_whiteboard(self) -> None:
        self.assert_route("先用白板做一个生产订单到入库的思维导图", "whiteboard-workbench")

    def test_precise_gif(self) -> None:
        self.assert_route("生成一个 UML 架构 SVG 和 GIF，检查几何与标签", "precise-technical-graphic")

    def test_explainer_set(self) -> None:
        self.assert_route("把这篇论文做成 6 张 16:9 中文技术解读图，保留事实台账", "explainer-image-set")

    def test_interactive_chart(self) -> None:
        self.assert_route("用真实数据做一个可交互的 Chart.js 经营指标组件", "interactive-widget")

    def test_interactive_timeline_stays_widget(self) -> None:
        self.assert_route("做一个可交互的时间线 HTML 组件", "interactive-widget")

    def test_animation(self) -> None:
        self.assert_route("把这段科普内容做成可录屏的仿 PPT 动画网页", "animated-explainer-html")

    def test_custom_editor(self) -> None:
        self.assert_route("开发一个 React + X6 的业务拓扑图编辑器，支持节点边端口事件", "custom-graph-application")

    def test_generic_request_needs_clarification(self) -> None:
        plan = build_plan("帮我画个图")
        self.assertTrue(plan["needs_clarification"])

    def test_editable_pptx_companion_is_explicit(self) -> None:
        plan = build_plan("把这个 SVG 转成可编辑 PPTX，并在每次图形输出时附带一份")
        self.assertTrue(plan["editable_pptx_companion"]["requested"], plan)
        self.assertEqual(plan["route"], "editorial-document")
        self.assertIn("native editable PPTX companion", plan["output_contract"][-1])


if __name__ == "__main__":
    unittest.main()
