---
name: lvsea-draw
description: "中文优先的终极 Draw 总调度 Skill：为系统架构图、流程图、时序图、数据流图、状态机、UML、ER、思维导图、白板草图、可编辑 Draw.io、Excalidraw、SVG/PNG/GIF、交互式 HTML、知识图谱、技术解读图和动画演示选择最合适的本地或外部绘图工作流，保留事实与可编辑源文件并完成验证。Use when users ask to 画图、制作架构图、流程图、可视化、技术解读图、动态 HTML、白板或把多个绘图 Skill 统一派发。"
---

# Lvsea Draw Boss

将本 Skill 当作绘图与可视化任务的总调度层，不把所有项目源码复制进来，也不默认同时调用所有工具。先判定用户真正要交付的东西，再选择一个主路由、至多两个协作路由，最后统一做事实、结构、渲染和视觉验收。

## 1. 先锁定交付契约

从用户请求中提取以下字段；信息已经足够时直接执行，不要为了形式追问：

- 目的：解释、评审、培训、汇报、白板讨论、编辑、发布或交互探索。
- 内容来源：代码仓库、文档或论文、用户给出的结构、数据表、图片，还是自由构想。
- 关系类型：架构、流程、时序、数据流、生命周期、层级、对比、时间线、UML/ER、协议或知识图谱。
- 目标形态：独立 HTML、SVG/PNG/GIF、Draw.io XML、Excalidraw JSON、Drawnix 白板文件、技术解读图片组、PPT/单页文档或可运行 Web 图编辑器。
- 编辑性：只读分享、可继续修改、需要浏览器实时预览，或需要在本地白板中手工调整。
- 质量等级：快速草图、普通交付、证据优先或发布级。

只有当来源、目标格式或关键事实缺失会改变主路由时才问一个聚焦问题。没有明确指定时，中文、可继续编辑、可迁移到项目目录的真实文件、紧凑高信息密度和实际验证是默认值。

## 2. 选择路由

先运行 scripts/route_request.py 做机器可读初判，或按 references/route-playbook.md 手动判断。路由名称和主 Skill 如下：

| 路由 | 典型请求 | 主执行器 |
| --- | --- | --- |
| codebase-knowledge-graph | 看懂仓库、代码关系、业务域、变更影响、入职导览 | $understand 及其 understand-* 子 Skill |
| evidence-architecture | 真实仓库架构、调用链、CI/CD、审批、数据血缘、生命周期 | $archify |
| precise-technical-graphic | SVG/PNG、UML、ER、云部署、事件流、可靠性、生成 GIF | $fireworks-tech-graph |
| editable-drawio | 明确要求 draw.io、drawio XML、云厂商图标、实时 Draw.io 编辑 | $bruce-drawio；若发现 Draw.io MCP，再调用其会话工具 |
| whiteboard-workbench | 白板、思维导图、自由画、Mermaid 转图、先讨论结构再定稿 | $drawnix |
| handdrawn-argument | 手绘感、Excalidraw、概念教学、视觉论证、证据卡片 | $excalidraw-diagram |
| explainer-image-set | 仓库或论文转 16:9 技术解读图、图组、事实台账、提示词包 | $technical-explainer-illustrator |
| interactive-widget | 交互式 HTML/SVG、Chart.js、矩阵、时间线、计算器、轻量 dashboard | $generative-ui-mcp |
| animated-explainer-html | 科普演示网页、仿 PPT 轮播、流程动画、录屏配套 HTML | $science-content-ppt 或本机等价 AI Animation Skill |
| editorial-document | 一页纸、白皮书、PPT/Slides 中的图、报告内嵌图解 | $kami；未安装时转本机可用的文档或 Slides Skill |
| custom-graph-application | 用户要开发可交互图编辑器、业务拓扑应用、React/Vue/SVG 图组件 | 使用 X6 作为工程库，进入代码实现路线，不把 X6 当成现成 Agent Skill |
| preview-and-qa | 只要求预览、检查 SVG、核对裁切或浏览器显示 | 使用本地浏览器或 SVG 预览工具；它不是绘图生成器 |

路由优先级：

1. 用户明确指定可编辑格式或工具时，先尊重该格式。
2. 真实代码仓库优先经过 codebase-knowledge-graph 或 evidence-architecture，不能凭目录名猜拓扑。
3. SVG/PNG/UML/GIF 的几何可靠性优先 precise-technical-graphic。
4. 解释图组优先 explainer-image-set；单张可交互组件优先 interactive-widget。
5. 白板草图和最终工程图分开处理：Drawnix 用于结构探索，不自动冒充最终定稿。
6. 只在有明确收益时增加协作路由；不要把多个产物揉成一张信息过载的图。

## 3. 路由执行规则

主路由执行前先读取对应 Skill 的入口说明和本仓库相关参考，不假设其他 Skill 已经热加载。执行过程中遵守以下规则：

- codebase-knowledge-graph：确认图谱数据目录、图谱 commit 与当前项目范围；有未分析的工作树变更时先警告。需要漂亮的可分享系统地图时，再把已核对关系交给 $archify。
- evidence-architecture：优先使用 Typed JSON IR、确定性校验和独立 HTML；架构、workflow、sequence、dataflow、lifecycle 不混为一个模式。只把作者定义的关系写成拓扑，不把图上可达性说成线上运行影响。
- precise-technical-graphic：先生成候选 SVG，再跑结构和几何检查，导出 PNG 后回读图片；只有用户明确要求动效时才生成 GIF，并保留 motion report。
- editable-drawio：保留 XML 或 .drawio 源文件、页面和版本历史；若实时浏览器会话或 MCP 未实际可用，改为输出可导入文件并明确标记。
- whiteboard-workbench：启动或使用 Drawnix 时核对端口；重要白板主动导出 .drawnix/JSON/PNG 到项目目录，不把浏览器缓存当正式资产。
- handdrawn-argument：技术主题先研究真实事件、字段、接口和示例；优先用视觉模式表达关系，并执行渲染-查看-修复循环。
- explainer-image-set：建立 SOURCE-MANIFEST、CLAIM-LEDGER 和 VISUAL-PLAN；每张图独立选择 reuse、deterministic、generate 或 hybrid 路线。
- interactive-widget：遵守 viewBox、字号、颜色阶、真实控件驱动和无外部不必要依赖；数据图表缺数据时不编造数值。
- animated-explainer-html：按旁白或内容节拍组织页面；检查动画可重复播放、响应式、安全区和录屏可用性。
- editorial-document：先锁内容、受众、页数、格式和视觉验收；图解必须服务页面主张，不能用装饰性图形填空白。
- custom-graph-application：先确认是否真的需要工程化编辑器；抽取 X6 的节点、边、端口、事件、插件和 SSR 能力，不为了画一张图引入整套应用。

## 4. 统一质量门

交付前按风险执行，不用一个重量级流程阻塞所有小草图：

1. 事实门：来源、版本、数字、名称、接口和关系可回溯；推论单独标记。
2. 源文件门：交付独立可编辑源文件；导出图只是派生物。
3. 确定性门：先做 XML/JSON/schema/几何/文件读取检查，再做浏览器或图片视觉检查。
4. 版式门：无文字越界、箭头穿框、标签重叠、裁切、孤字、无效留白和不可读字号。
5. 交互门：按钮、缩放、搜索、播放、导出或控件必须真的改变视图；没有实际调用就不要声称可用。
6. 可迁移门：正式数据和附件放在项目目录真实文件中；不要把 localStorage、IndexedDB 或浏览器缓存当备份。
7. 交付门：说明主文件、源文件、派生文件、验证命令、实际运行状态和外部阻塞。

视觉审美以用户当前请求、指定模板和已有设计规则为最高优先级。默认采用中文、信息密度高但留白有目的、控件直接、颜色克制、字号可读的工作台式输出；党政或制造管理材料优先庄重、清晰、低噪声，不默认使用霓虹、廉价渐变或装饰卡片堆叠。

## 5. 失败与降级

- Archify 不可用：技术 HTML 可退到 Fireworks SVG/PNG，轻量 HTML 可退到 Generative UI。
- Fireworks 不可用：使用 Archify 的可验证 HTML，或手工确定性 SVG；不要声称已经完成几何验收。
- Draw.io MCP 不可用：调用本地 bruce-drawio 输出 XML；不能声称浏览器实时预览已打开。
- Drawnix 不可用：输出 Excalidraw JSON 或 HTML 草图，并说明没有白板会话。
- 生图工具不可用：Technical Explainer Illustrator 仍可交付来源清单、事实台账、视觉计划、确定性图形和提示词包。
- X6 不存在于运行时：只保留工程设计和实现建议，不伪造可运行 Web 图编辑器。
- 任何视觉检查无法进行时：写 visual_review: skipped，并把风险交给用户，不猜测通过。

## 6. 中文调用示例

- 用 $lvsea-draw 分析这个生产管理仓库，先生成代码知识图谱，再给出一张有证据的运行时架构图，保留可编辑源文件。
- 用 $lvsea-draw 把安全生产异常闭环做成可继续修改的 Draw.io 流程图，同时导出 SVG 和 PNG，检查文字与箭头。
- 用 $lvsea-draw 把这篇技术报告拆成 6 张 16:9 中文技术解读图，先建立事实台账，所有数字保留来源定位。
- 用 $lvsea-draw 把这段制造工艺流程做成可直接打开的交互式 HTML，加入步骤播放、分支高亮和 SVG 导出，但不要编造工艺参数。

路由回归样例在 evals/trigger_cases.json 和 evals/semantic_config.json，标准库路由器和单元回归在 scripts/route_request.py 与 tests/test_route_request.py。

## 中文使用说明

输入可以是中文自然语言、代码仓库路径、GitHub URL、Markdown、Mermaid、PDF/Word/网页正文、数据文件、图片或已有图源。主要产物由路由决定，至少应包含一个可继续编辑的源文件、必要的渲染结果和验证记录。需要了解具体判断或降级方式时，读取 references/route-playbook.md、references/source-matrix.md、references/quality-contract.md 和 references/local-adapters.md。

## 注意事项、限制与能力边界

- 本 Skill 是派发与质量总线，不替代每个专业绘图 Skill，也不凭空提供未安装的 MCP、浏览器会话、模型、生图 API 或外部凭据。
- 外部仓库、私有代码和在线资料必须按当前授权读取；不复制上游源码、图片、商标或受保护模板，只抽取可复用方法。
- 图上的结构不等于真实运行时状态；生产部署、风险、性能、合并安全和业务结论需要独立证据。
- 发布前必须同时区分静态可发现、实际可调用、渲染通过、浏览器验证和 GitHub 推送成功。
