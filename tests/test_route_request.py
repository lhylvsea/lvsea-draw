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

    def test_codebase_graph(self) -> None:
        self.assert_route("分析这个 GitHub 仓库，生成可搜索的代码知识图谱和变更影响", "codebase-knowledge-graph")

    def test_drawio_wins_over_generic_flow(self) -> None:
        self.assert_route("把安全生产异常闭环做成可继续修改的 Draw.io XML", "editable-drawio")

    def test_whiteboard(self) -> None:
        self.assert_route("先用白板做一个生产订单到入库的思维导图", "whiteboard-workbench")

    def test_precise_gif(self) -> None:
        self.assert_route("生成一个 UML 架构 SVG 和 GIF，检查几何与标签", "precise-technical-graphic")

    def test_explainer_set(self) -> None:
        self.assert_route("把这篇论文做成 6 张 16:9 中文技术解读图，保留事实台账", "explainer-image-set")

    def test_interactive_chart(self) -> None:
        self.assert_route("用真实数据做一个可交互的 Chart.js 经营指标组件", "interactive-widget")

    def test_animation(self) -> None:
        self.assert_route("把这段科普内容做成可录屏的仿 PPT 动画网页", "animated-explainer-html")

    def test_custom_editor(self) -> None:
        self.assert_route("开发一个 React + X6 的业务拓扑图编辑器，支持节点边端口事件", "custom-graph-application")

    def test_generic_request_needs_clarification(self) -> None:
        plan = build_plan("帮我画个图")
        self.assertTrue(plan["needs_clarification"])


if __name__ == "__main__":
    unittest.main()
