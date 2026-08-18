# lvsea-draw 中文使用说明

## 中文触发词

- 画架构图、流程图、时序图、数据流图、状态机、UML、ER 图
- 做系统可视化、技术解读图、仓库架构图、代码知识图谱
- 做 Draw.io、Excalidraw、Drawnix 白板、SVG、PNG、GIF 或交互式 HTML
- 把论文、README、技术报告、制造流程、安全闭环转成图
- 生成动画流程图、仿 PPT 演示网页、交互式组件或图编辑器
- 做信息图、数据故事、信息长图、时间线/对比/漏斗/金字塔/列表信息图
- 用 AntV Infographic DSL、Agents365 drawio-skill 或 diagram-design 生成图
- 按品牌规范把 Mermaid/Draw.io 重绘成自包含 HTML、可访问 SVG 或 PNG
- 把多个绘图 Skill 统一路由、派发、验证和发布
- 把 SVG 或静态 HTML 图转成原生可编辑 PPTX，或要求每次视觉输出附带一份 PPTX

## 中文使用说明

这是一个绘图类垂直 Agent 的总调度 Skill。它先抽取目的、来源、关系类型、目标格式、编辑性和质量等级，再选择一个主路由，必要时增加一个协作路由。主路由可以是本机已安装的 archify、fireworks-tech-graph、drawnix、bruce-drawio、excalidraw-diagram、technical-explainer-illustrator、generative-ui-mcp、understand 或 science-content-ppt，也可以是用户明确要求的外部 MCP 或 X6 工程实现。只要主路由产出 canonical SVG 或静态 HTML，就再调用 `scripts/emit_editable_pptx.py` 生成一份原生可编辑 PPTX 伴随物。

建议流程：

1. 说明想解释什么、给谁看、最终要什么格式。
2. 提供代码仓库、文件、URL、正文、Mermaid、数据或已有图源。
3. 让 lvsea-draw 先输出路由判断；请求足够清楚时直接继续执行。
4. 保留 JSON、XML、SVG、.drawnix、.excalidraw、HTML 或工程源文件。
5. 先做确定性检查，再做浏览器或图片视觉检查。
6. 交付文件路径、主要验证结果和尚未验证的外部条件。

信息图请求先进入 `infographic-composition`：抽取标题、说明、主数据族、语言、图标和主题，再选择 sequence/list/compare/hierarchy/chart/relation 模板，保留 Infographic DSL。若本机没有 AntV 运行时，转 `editorial-diagram` 或 `precise-technical-graphic`，并在交付状态中说明降级。

品牌化静态图、Mermaid/Draw.io 重绘进入 `editorial-diagram`，先按 diagram-design 的语义模式、信息密度、尺寸和 style guide 处理，默认交付自包含 HTML 与可访问 SVG。需要放进 PPT 或报告时，再由 `editorial-document` 负责页面排版。

科研汇报、工作汇报或用户明确说“SVG 转可编辑 PPTX”时，主图源仍按内容语义路由；图源完成并通过结构/视觉检查后，用 `emit_editable_pptx.py` 追加 PPTX、对象检查报告和转换 trace。PPTX 失败时保留主图源并报告 `blocked`，不能用图片嵌入 PPT 冒充可编辑。

明确要 `.drawio`、代码/IaC/SQL/OpenAPI 导入或 Draw.io CLI 时，进入 `editable-drawio`，优先 drawio-skill；只有现场探测到 CLI、Graphviz 和实际导出，才把 PNG/SVG/PPTX 写成已验证产物。

## 四个真实应用场景

1. 生产订单到批次、检验、入库的制造管理流程：先白板讨论，后输出 Draw.io 或 Archify 正式图。
2. 安全生产异常上报到关闭的闭环：保留责任边界、异常分支和复盘节点，导出可编辑源文件与 PNG。
3. GitHub 仓库转成架构总览、核心机制和依赖关系图：先知识图谱或证据台账，再做技术解释图。
4. 带指标的工艺或经营数据可视化：用交互式 HTML/Chart.js 展示真实数据，缺失数据只显示待补字段。
5. 三级干燥或其他科研工艺流程汇报：保留温度段、含水率、分流比例和能耗结论，输出 SVG/PNG 后再附一份原生可编辑 PPTX，并单独回读首张幻灯片。

## 产物

- 路由 JSON：route、secondary_routes、reasons、output_contract、validation 和 fallback。
- 可编辑源文件：根据路由生成 JSON、XML、SVG、HTML、.drawnix、.excalidraw 或 Web 工程。
- 信息图源文件：Infographic DSL、模板/主题记录和独立 HTML/SVG；若使用降级路线，保留原始结构说明。
- 派生文件：PNG、SVG、GIF、WebM、PDF、PPT 或图片组。
- 静态视觉的 PPTX 伴随文件：原生 DrawingML `.pptx`、`-svg-quality.json`、`.trace.json` 和汇总 `.report.json`；图片对象仍保留为图片。
- 证据与 QA：来源清单、事实台账、视觉计划、渲染报告或人工检查记录。

## 注意事项、限制与能力边界

- 没有实际 MCP、浏览器、端口、模型、凭据或渲染器时，必须写明“已配置但未实际调用”或“静态通过但交互未验证”。
- 图上的关系不自动等于线上拓扑、风险结论、性能结论或业务事实。
- Drawnix 的浏览器缓存不是正式备份；重要白板要导出到项目目录。
- SVG/PNG/GIF 的质量不能只靠文本或 XML 检查；需要实际渲染和图片回读。
- 技术图中的数字、公式、接口、协议和架构关系必须绑定来源；不能用图像模型替代事实核对。
- AntV Infographic、drawio-skill 和 diagram-design 的上游包、CLI、Skill、浏览器或品牌配置是否可用，必须按本次运行重新探测。
- 公开上游的源码、图片和品牌资产只做方法研究，不复制到本 Skill。
- PPT Master、LibreOffice、Poppler 或字体未发现时，不能声称 PPTX 已完成；必须记录实际发现状态、导出状态和视觉预览是否执行。
- HTML 转 PPTX 只提取第一个静态内联 SVG；交互、动画、Canvas、WebGL 和外部动态数据不会自动变成可编辑 PPT 对象。
