---
name: lvsea-draw
description: "中文优先的 Draw 总调度 Skill：根据来源、关系语义、编辑性、目标格式和质量风险，为架构图、流程图、时序图、数据流图、UML、信息图、白板、Draw.io、Excalidraw、Mermaid、SVG/PNG/GIF、HTML、知识图谱和技术解读图选择合适的本地或外部工作流，保留事实与可编辑源文件并完成验证；静态 SVG/HTML 视觉默认追加一份原生可编辑 PPTX 伴随产物。Use when users ask to 画图、制作架构图、流程图、信息图、可视化、技术解读图、白板、Mermaid 美化、Mermaid 主题/配色/渲染、Pretty Mermaid、AntV Infographic、diagram-design、drawio-skill、SVG 转可编辑 PPTX，或统一派发多个绘图 Skill。"
---

# Lvsea Draw Boss

绘图与可视化总调度层。先判断真正的交付物，再选一个主路由、至多两个协作路由；不把未发现、未调用或未验证的工具写成已完成。

## 触发与输入

触发词包括：架构图、流程图、时序图、数据流图、信息图、数据故事、技术解读图、白板、Draw.io、Excalidraw、Mermaid、Mermaid 美化、主题、配色、渲染、图表太寡淡、Pretty Mermaid、SVG/PNG/GIF、交互式 HTML、图编辑器、可编辑 PPTX、SVG 转 PPTX、每次附带 PPTX。

从请求中提取：目的与受众、来源、关系语义、目标格式、编辑性、证据风险和交付目录。没有关键缺口时直接执行；默认中文、真实项目文件、可继续编辑、16:9、高信息密度和实际验证。

## 路由

- 代码仓库关系：`codebase-knowledge-graph` → Understand。
- 真实架构/流程/调用链：`evidence-architecture` → Archify。
- 几何可靠 SVG/PNG/UML/GIF：`precise-technical-graphic` → Fireworks。
- Draw.io/XML：`editable-drawio` → drawio-skill，缺失时明确降级。
- 白板/思维导图/手绘论证：`whiteboard-workbench` / `handdrawn-argument`。
- 信息图/数据故事：`infographic-composition`；品牌静态图：`editorial-diagram`。
- Mermaid 已能渲染但过于寡淡：`mermaid-polish` → Pretty Mermaid；需要品牌规范、可访问 SVG 或自包含 HTML 时协作 `editorial-diagram`。
- 交互组件/动画网页：`interactive-widget` / `animated-explainer-html`。
- PPT/报告版式：`editorial-document`，图形本体仍交给更合适的图形路由。
- 仅预览检查：`preview-and-qa`；要开发图编辑产品才进入 `custom-graph-application`。

先运行 `scripts/route_request.py`，再读取 `references/route-playbook.md`、对应适配器说明和主路由 Skill 的入口说明。

## 统一交付契约

保留源文件，再交付派生物；执行事实、结构、确定性、版式、交互、可迁移和视觉验收。下游返回 `source_artifact`、`rendered_artifacts`、`validation_commands`、`visual_review`、`missing_capabilities`、`fallback_used` 和 `remaining_risks`。

只要主路由产生 canonical SVG 或静态 HTML，必须追加：

```powershell
python scripts/emit_editable_pptx.py path/to/diagram.svg -o output/diagram-可编辑.pptx --render-preview
```

适配器发现本机 PPT Master，最小化处理 CSS/filter/箭头，运行 SVG quality gate 和 `svg_to_pptx.py --pptx-structure flat`，检查 PPTX ZIP、原生形状、文本、图片和可选渲染预览。PPTX、`-svg-quality.json`、`.trace.json` 和 `.report.json` 是新增伴随物，不替换 JSON、HTML、SVG、PNG 或 Draw.io/XML。没有 PPT Master、源图不兼容或导出失败时报告 `blocked`，不能静默省略。

触发回归位于 `evals/trigger_cases.json` 和 `evals/semantic_config.json`；使用它们验证新增的可编辑 PPTX 触发边界。

## 四个真实场景

1. 制造订单到入库：先白板讨论，再交付 Draw.io/Archify 正式流程图和 PPTX 伴随物。
2. 安全生产异常闭环：保留责任边界和异常分支，导出可编辑源、SVG/PNG 和 PPTX。
3. GitHub 仓库解读：先建知识图谱和事实台账，再生成架构图与可编辑 PPTX。
4. 科研工艺汇报：保留温度段、含水率、分流比例和能耗结论，输出 SVG/PNG/PPTX，并回读首张幻灯片。

## 边界

动态 HTML、Canvas、WebGL、图片组和未发现的 MCP/浏览器/凭据不能直接声称可编辑或已调用；HTML 转 PPTX 只提取首个静态内联 SVG。PPTX 的“可编辑”仅覆盖 PPT Master 支持的 SVG 文本和几何对象，嵌入图片仍是图片。详细路由、质量、适配器和 PPTX 契约见 `references/`；发布前区分静态可发现、实际调用、渲染通过、视觉验证和 GitHub 推送成功。
