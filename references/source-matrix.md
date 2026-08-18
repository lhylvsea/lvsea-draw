# 上游能力矩阵

研究日期：2026-08-18。用户给出的 excalidraw-diagram-skill 链接重复出现一次，按一个来源处理。下表记录的是能力抽取，不是把上游源码或素材打包进 lvsea-draw。

| 来源与研究快照 | 保留的精华 | 不直接采用 | 默认路由 |
| --- | --- | --- | --- |
| [Archify](https://github.com/tt-a1i/archify)，5875dc81 | 五种技术图语义、Typed JSON IR、schema/layout/route/label 净空检查、最后一次可信输出、独立 HTML 和多格式导出；源码证据按需绑定版本与行号 | 不把它当通用 WYSIWYG 白板；不把图上可达性说成线上影响；不强行启用 deployment ownership | evidence-architecture |
| [Generative-UI-MCP](https://github.com/op7418/Generative-UI-MCP)，5accf126 | interactive、chart、mockup、art、diagram 模块按需加载；streaming-safe 顺序、颜色阶、SVG viewBox 和真实控件驱动 | 不用它替代深度工程图、后端系统或大型前端工程；MCP 未连接时使用本机内嵌规范 | interactive-widget |
| [Drawnix](https://github.com/plait-board/drawnix)，b0d682ce | 一体化白板、思维导图、流程图、自由画、插件机制、PNG/JSON 导出；适合先发散、讨论和人工调整 | 不把浏览器自动保存当正式跨电脑资产；不把白板草图自动冒充正式证据图 | whiteboard-workbench |
| [Next AI Draw.io](https://github.com/DayuanJiang/next-ai-draw-io)，96bca2b | AI 生成和修改 Draw.io XML、图片/PDF/文本输入、历史版本、实时浏览器预览、MCP 工具和 .drawio/SVG/PNG 导出 | 不声称默认模型、实时会话或浏览器已可用；密钥、MCP、端口和 draw.io embed 要现场核对 | editable-drawio |
| [Kami](https://github.com/tw93/Kami)，8bf6f46 | 内容先行、材料检查、执行契约、文档/单页/PPT 版式、内嵌 SVG 图解、渲染前后检查和风格克制 | 不把文档排版 Skill 误当系统图编辑器；当前机器未发现直接 kami 入口时不虚构调用 | editorial-document |
| [Fireworks Tech Graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)，50c819d | SVG/PNG 几何检查、12 套风格、14 类 UML、离线 HTML、语义 GIF、结构检查加 PNG 回读的双重 QA | 不用于照片、普通艺术图和量化数据图；GIF 只在受支持的语义合同和用户明确要求时生成 | precise-technical-graphic |
| [Excalidraw Diagram Skill](https://github.com/coleam00/excalidraw-diagram-skill)，8646fcc | 图形要表达论证而非罗列；深度评估、真实证据 artifact、多层缩放、形状语义、分段生成和 render-view-fix | 不用统一卡片网格替代视觉关系；精确几何、工程级导出优先转 Fireworks 或 Archify | handdrawn-argument |
| [AntV X6](https://github.com/antvis/X6)，bb173c1 | HTML/SVG/React/Vue/Angular 节点、边、端口和事件自定义，插件生态，服务端渲染，适合做业务图编辑应用 | 不把库当成现成 Agent Skill；用户只要一张图时不引入整套工程 | custom-graph-application |
| [Technical Explainer Illustrator](https://github.com/lhylvsea/technical-explainer-illustrator)，7c6843a | SOURCE-MANIFEST、CLAIM-LEDGER、VISUAL-PLAN；reuse/deterministic/generate/hybrid 逐图路由；图片 QA 和无生图降级 | 生成式图片不承担精确数字、接口、架构关系；不复制原文图片、水印或品牌资产 | explainer-image-set |
| [Understand Anything](https://github.com/Egonex-AI/Understand-Anything)，fe8c5bc | 多智能体代码解析、文件/函数/类/依赖图、语义搜索、引导式学习、业务域视图、增量更新和变更影响 | 没有新鲜图谱时不直接用旧图得出结论；它负责理解代码，不替代最终视觉编排 | codebase-knowledge-graph |
| [SVG Preview](https://uutool.cn/svg-preview/)，页面检查于 2026-08-11 | 快速打开、解析和人工检查 SVG 的低成本入口 | 不把预览页当 SVG 生成器、结构校验器或正式部署 | preview-and-qa |
| [AI Animation](https://github.com/Unclecheng-li/AI_Animation)，8c79ee5 | 多个 HTML 动效 Skill：PPT 轮播、流程/原理演示、协议可视化、动态架构、学霸笔记和卡片剧场；重视动画重置和录屏 | 不用模板动画替代事实台账；动画页面不是可编辑图编辑器或工程拓扑验证器 | animated-explainer-html |

| [AntV Infographic](https://github.com/antvis/Infographic)，69eae2ee | 声明式、AI 友好的 Infographic DSL；template/data/theme 分层；list/sequence/compare/hierarchy/relation/chart 结构族；模板、主题、编辑器和 SVG 输出思路 | 不复制上游模板、运行时代码、图标和站点素材；不把可选 CDN 或未安装 Skill 写成离线渲染能力 | infographic-composition |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill/)，2ee141e0 | 11 类 Draw.io 预设；Mermaid、代码库、Terraform/Kubernetes、SQL/OpenAPI、C4 导入；官方图形/云图标检索；自检、自动修复、多页、viewer、热力图和导出策略 | 不复制 Skill 源码、脚本、图标库或桌面 CLI；不在未探测 CLI/Graphviz/版本时声称导入、PNG/SVG/PPTX 成功 | editable-drawio |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)，e48df3fb | 27 种静态图类型；语义模式优先；自包含 HTML、可访问 SVG、尺寸/受众/细节调节；品牌 style guide 首次确认门；Mermaid/Draw.io 重绘与可选可访问动效 | 不复制模板、图标、品牌资产或上游默认主题；不把“静态结构检查”当作浏览器/图片视觉通过 | editorial-diagram |

## 组合原则

1. Understand Anything 负责从真实代码中建立可检索关系，Archify 负责把已核对关系变成可分享的工程地图。
2. Drawnix 负责白板阶段，Draw.io 负责 XML 可编辑交付，Fireworks 负责几何可靠的 SVG/PNG/GIF。
3. Technical Explainer Illustrator 负责成套解释图片和事实台账，Generative UI 负责轻量交互组件。
4. Excalidraw 负责手绘论证和教学结构，AI Animation 负责有限叙事动效，Kami 负责图解进入正式文档的版式。
5. X6 只在“要开发图编辑产品”时成为工程底座；SVG Preview 只在预览和人工核对阶段使用。

6. Infographic 负责信息结构和 DSL 源文件，diagram-design 负责品牌化、可访问的静态图；两者共享事实台账，但不混写源格式。
7. drawio-skill 负责可编辑 `.drawio` 和代码/IaC/SQL/OpenAPI 导入；CLI、Graphviz、版本与导出是独立能力门，不因 XML 生成通过而自动通过。
8. Diagram Design 的“删除无效节点、控制密度、每条连线有语义、首次品牌确认”补强所有静态图路线；它不是用装饰替代关系的模板机。

## 研究边界

上游 README、SKILL.md、参考文档和当前公开仓库只用于识别能力与边界。没有在本次研究中把所有上游运行时都实际部署；实际调用、端口、浏览器、MCP、模型和第三方依赖以本地适配器探测和本次任务验证为准。
