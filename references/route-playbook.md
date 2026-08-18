# 路由手册

## 输入维度

将请求拆成五个维度：

| 维度 | 取值示例 | 对路由的影响 |
| --- | --- | --- |
| 来源可信度 | repo、文档、数据、用户结构、自由构想 | repo/文档触发事实核对；自由构想可以先做草图 |
| 关系语义 | architecture、workflow、sequence、dataflow、lifecycle、tree、matrix、UML、protocol | 决定图形模型，不让所有请求落到流程图 |
| 交付格式 | HTML、SVG/PNG/GIF、drawio、excalidraw、drawnix、PPT、图片组、Web app | 用户指定格式优先于默认美学 |
| 交互程度 | 静态、finite motion、viewer、whiteboard、live edit | 选择 Archify、Fireworks、Drawnix、MCP 或 X6 |
| 证据风险 | 低、普通、事实关键、发布级 | 决定是否必须建立 claim ledger、源码行号、视觉回读和复核记录 |

## 决策树

新增路由的优先级规则：

- 明确要求信息图、数据故事、信息长图、对比/时间线/漏斗/金字塔/列表信息图或 Infographic DSL：`infographic-composition`。
- 明确要求品牌化静态图、样式指南、Mermaid/Draw.io 重绘、可访问 HTML/SVG 或 diagram-design：`editorial-diagram`。
- 如果同时明确要求 `.drawio` 或 Draw.io 编辑，格式约束优先，主路由仍为 `editable-drawio`，信息图或品牌图作为协作路由。
- 如果请求是“把图放进 PPT/报告/一页纸”，`editorial-document` 负责版式，图形本体仍交给信息图或编辑图路由。

1. 明确要求 Draw.io、.drawio、XML、云厂商图标或 Draw.io 实时编辑：editable-drawio。
2. 明确要求白板、思维导图、自由画或先讨论结构：whiteboard-workbench。
3. 明确要求 Excalidraw、手绘、草图、概念教学或视觉论证：handdrawn-argument。
4. 明确要求仓库知识图谱、搜索、导览、业务域或变更影响：codebase-knowledge-graph。
5. 输入真实代码并要求系统地图、调用链、数据流、生命周期或架构评审：evidence-architecture。
6. 明确要求 SVG、PNG、UML、ER、GIF、几何可靠、离线交互 HTML：precise-technical-graphic。
7. 明确要求论文/README/报告/仓库转成多张 16:9 技术解读图：explainer-image-set。
8. 明确要求 dashboard、chart、calculator、widget、轻量 HTML/SVG：interactive-widget。
9. 明确要求动画网页、仿 PPT、录屏配套流程演示：animated-explainer-html。
10. 图解属于一页纸、PPT、白皮书、报告或 landing page：editorial-document，并把图形子任务交给更合适的路由。
11. 明确要开发可编辑图产品、节点/边/端口/事件和业务交互：custom-graph-application。
12. 只要求打开、预览、检查 SVG：preview-and-qa。
13. 仍然不明确时，只问一个问题：最终要可编辑文件、可直接打开的 HTML，还是图片/PPT？

## 主路由与协作路由

| 主路由 | 可以协作 | 不要做 |
| --- | --- | --- |
| codebase-knowledge-graph | evidence-architecture、explainer-image-set | 不要跳过图谱 freshness 检查 |
| evidence-architecture | precise-technical-graphic、editorial-document | 不要将图上路径写成线上影响 |
| precise-technical-graphic | preview-and-qa、editorial-document | 不要把结构检查等同视觉通过 |
| editable-drawio | preview-and-qa、editorial-document | 不要在没有会话时声称实时预览 |
| whiteboard-workbench | editable-drawio、evidence-architecture | 不要让浏览器缓存成为唯一资产 |
| handdrawn-argument | explainer-image-set、preview-and-qa | 不要用装饰替代关系和证据 |
| explainer-image-set | evidence-architecture、precise-technical-graphic | 不要让生成图承载精确事实 |
| interactive-widget | editorial-document、animated-explainer-html | 不要生成没有真实交互的假控件 |
| animated-explainer-html | interactive-widget、editorial-document | 不要让动效掩盖内容不足 |
| editorial-document | 任一图形主路由 | 不要先套模板再压缩事实 |
| custom-graph-application | evidence-architecture | 不要为单张图引入过重工程 |
| preview-and-qa | 触发原主路由修复 | 不要把在线预览工具当生成器 |

协作上限默认是一个主路由加一个协作路由。只有用户明确要成套产物，或主路由的输出本来就是组合契约时，才增加第二个协作路由。

### 新增 provider 协作

| 主路由 | 首选 provider | 协作或降级 | 关键约束 |
| --- | --- | --- | --- |
| infographic-composition | AntV Infographic / `antv-infographic` | diagram-design、precise-technical-graphic、interactive-widget | 保留 DSL；模板与主数据族必须匹配；没有真实 AntV 运行时不得声称已渲染 |
| editable-drawio | Agents365 `drawio-skill` | `bruce-drawio`、Draw.io MCP | `.drawio` 是源文件；CLI/Graphviz/版本/导出逐项探测 |
| editorial-diagram | `diagram-design` | infographic-composition、precise-technical-graphic、editorial-document | 先语义模式、密度和 style guide，再输出自包含 HTML/SVG |

## 统一派发协议

派发给下游 Skill 时，附带以下上下文：

- intent：用户要解决的问题和目标受众。
- source：来源路径/URL、版本、读取时间和可信级别。
- relation_model：节点、边、方向、分支、状态或数据字段。
- output_contract：源文件、派生文件、尺寸、格式、编辑方式和验收标准。
- evidence_policy：哪些内容必须引用，哪些内容可以是明确标记的推断。
- qa_budget：需要结构检查、渲染、截图、图片回读或人工检查到什么程度。

下游返回时必须回收：

- source_artifact；
- rendered_artifacts；
- validation_commands；
- visual_review；
- missing_capabilities；
- fallback_used；
- remaining_risks。

## 典型组合

### 仓库解读图

Understand Anything → 核对图谱和当前变更 → Archify → 可选 Technical Explainer 图组。

### 制造流程正式图

Drawnix 讨论草图 → 用户确认结构 → Draw.io XML 或 Archify Workflow → Fireworks SVG/PNG。

### 技术文章动态教学页

Technical Explainer 建事实台账 → Generative UI 生成静态图解组件或 AI Animation 生成叙事页 → 浏览器截图和动画重复播放检查。

### 业务拓扑编辑器

先交付内容模型和路由契约 → X6 工程实现节点/边/端口/事件 → 浏览器交互测试和导出测试；这不是一次性图生成任务。

### 信息图和品牌图

结构化培训要点、指标对比或阶段路线：先由 `infographic-composition` 生成可复核的 DSL，再按本机可用能力渲染 HTML/SVG；需要企业品牌、可访问静态图或 Mermaid/Draw.io 重绘时，增加 `editorial-diagram`，不要把两种源文件混成不可维护的单一产物。

代码库、Terraform/Kubernetes、SQL 或 OpenAPI 的正式可编辑图：先由 `drawio-skill` 解析并生成 `.drawio`，再执行 XML/边引用/CLI/PNG 回读检查；没有 CLI 时可以交付源文件，但必须标记导出未验证。

## 不应触发

翻译、普通摘要、单纯解释“什么是流程图”、一次性文案、只要求看一张已有图片而不修改，以及明确说不要创建或执行绘图产物的请求，不应被 lvsea-draw 抢占。
