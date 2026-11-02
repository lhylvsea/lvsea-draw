# lvsea-draw

中文优先的架构图、流程图、Mermaid 美化、可视化图和技术解释图总调度 Skill。它不把所有绘图工具硬拼成一个渲染器，而是根据用户意图、事实来源、编辑格式、交互要求和质量风险，把任务派发给最合适的本地 Skill、MCP 或工程库，再统一完成验证与交付。

## 定位

lvsea-draw 是一个垂类 Agent 派发层，核心职责是：

- 选择正确的图形语义，而不是所有请求都画成流程图。
- 在 Archify、Fireworks、Draw.io、Drawnix、Excalidraw、Technical Explainer、Generative UI、Understand Anything、AI Animation 和文档排版路线之间做选择。
- 对 Mermaid 已能渲染但主题寡淡、配色弱、边线和标签不清的请求，优先派发 `mermaid-polish`，使用 Pretty Mermaid 生成有主题的 SVG、PNG 或终端 ASCII；保留 `.mmd` 源文件。
- 默认保留可编辑源文件，导出的 HTML、SVG、PNG、GIF、图片组或 PPT 作为派生物；静态 SVG/HTML 图形再追加一份原生可编辑 PPTX 伴随物。
- 对事实、结构、几何、渲染、交互和视觉质量分层验收。
- 工具、MCP、浏览器或凭据缺失时透明降级，不把“文件存在”写成“已经跑通”。

## 安装

### Codex 全局安装

把本仓库目录复制到：

~~~text
C:\Users\rabbit\.codex\skills\lvsea-draw
~~~

或使用本机的 Skill 安装方式将仓库作为 Agent Skill 安装。安装后重启 Codex，使新入口重新发现。

### 显式调用

~~~text
Use $lvsea-draw to route this request and deliver an editable, validated diagram.
~~~

中文最短调用：

~~~text
用 $lvsea-draw 选择最合适的绘图路线，保留可编辑源文件并完成验证。
~~~

## 路由概览

| 用户目标 | 主路由 | 适合的交付 |
| --- | --- | --- |
| 看懂真实代码库 | Understand Anything | 知识图谱、搜索、学习路径、变更影响 |
| 有证据的系统架构或流程 | Archify | Typed JSON、独立 HTML、PNG/SVG/WebM/分享卡 |
| 几何可靠的 SVG、PNG、UML、GIF | Fireworks Tech Graph | SVG、1920px PNG、离线 HTML、语义 GIF |
| 可编辑 Draw.io | Agents365 drawio-skill；缺失时 bruce-drawio 或 Draw.io MCP | .drawio/XML、PNG/SVG |
| 白板、思维导图、自由画 | Drawnix | 白板会话、.drawnix/JSON/PNG |
| 手绘视觉论证 | Excalidraw Diagram | .excalidraw JSON、证据卡片、教学结构 |
| 仓库或论文的成套技术解读图 | Technical Explainer Illustrator | 来源清单、事实台账、视觉计划、图片组、QA |
| 交互式小组件和数据图 | Generative UI MCP | 单文件 HTML、SVG、Chart.js、widget |
| 信息图和数据故事 | AntV Infographic；缺失时 diagram-design 或精确 SVG | Infographic DSL、HTML/SVG、PNG |
| 科普演示和动画 HTML | AI Animation / science-content-ppt | 仿 PPT 轮播、流程动画、录屏网页 |
| 图解嵌入一页纸、PPT、白皮书 | Kami 或本机文档 Skill | HTML/PDF/PPT/Slides 内嵌图解 |
| 品牌化静态图和 Mermaid/Draw.io 重绘 | cathrynlavery diagram-design | 自包含 HTML、可访问 SVG、可选 PNG |
| Mermaid 主题渲染和美化 | Pretty Mermaid | `.mmd`、主题 SVG、可选 PNG/ASCII；六类图和 15 个主题 |
| 开发业务图编辑器 | AntV X6 | React/Vue/SVG 图编辑工程 |

完整判断规则见 references/route-playbook.md。来源研究和取舍见 references/source-matrix.md。

## 可编辑 PPTX 伴随产物

当主路由输出 canonical SVG 或静态 HTML 时，Skill 会追加 `scripts/emit_editable_pptx.py`：它发现本机 PPT Master，做最小 SVG 兼容归一化，先跑 SVG quality gate，再生成原生 DrawingML PPTX，并写出对象检查、转换 trace 和可选首张预览。主 SVG/HTML/JSON/PNG 等文件不会被替换。

```powershell
python scripts/emit_editable_pptx.py path/to/diagram.svg `
  -o output/diagram-可编辑.pptx `
  --render-preview
```

“可编辑”只覆盖 PPT Master 支持的 SVG 文本和几何对象；嵌入图片仍是图片，动态 HTML 必须先输出静态 SVG。PPT Master 未发现、质量门失败或导出失败时，报告会写成 `blocked`，不会把图片嵌入 PPTX 冒充原生可编辑图。

## 本次新增整合

- **AntV Infographic**：把“信息图/数据故事/对比/时间线/漏斗/金字塔/列表”识别为信息结构任务，保留 DSL 源文件；AntV 运行时未实际可用时，按 provider policy 降级到 diagram-design 或精确 SVG，不伪造渲染状态。
- **Agents365 drawio-skill**：成为 editable-drawio 的优先 provider，覆盖 Mermaid、代码库、Terraform/Kubernetes、SQL/OpenAPI、C4、多页 `.drawio`、自检/自动修复和导出验证；桌面 CLI、Graphviz、版本和真实导出仍需现场探测。
- **cathrynlavery diagram-design**：新增 editorial-diagram 路由，优先静态、自包含、可访问和品牌可控的 HTML/SVG；先选语义模式和密度，再处理 style guide、尺寸和可选动效。

三份上游只贡献方法、路由和质量规则，不复制上游源码、模板、图片、图标库或品牌资产。固定研究版本见 [references/source-matrix.md](references/source-matrix.md)。

### Mermaid 美化示例

用户说“这张 Mermaid 已经画出来了，但太寡淡，请换成适合培训投屏的主题并输出 SVG/PNG”，路由会保留 `.mmd`，选择 Pretty Mermaid 的主题和颜色角色，调节节点/层级间距，检查 SVG/PNG 与长标签，再按静态 SVG 伴随规则尝试生成可编辑 PPTX。若用户要求品牌规范、可访问 SVG、自包含 HTML 或 `.drawio`，格式门会分别转给 `diagram-design` 或 `drawio-skill`。

## 四个真实场景

### 1. 制造运营系统架构

输入生产订单、批次、检验、入库等模块说明或真实代码库。先用 Understand Anything 检查文件、函数和依赖关系，再用 Archify 生成高层架构和一条主路径；如果需要 SVG/PNG 进入汇报，再转 Fireworks 做几何和视觉检查。

### 2. 安全生产异常闭环

输入事故上报、分级、处置、复盘和关闭规则。若需要现场讨论，先用 Drawnix 做可编辑白板；若要求正式可交付文件，用 Draw.io XML 或 Archify Workflow，并检查分支、异常路径、责任边界和文字可读性。

### 3. 技术报告转 16:9 图组

输入论文、README、技术报告或仓库。先建立 SOURCE-MANIFEST、CLAIM-LEDGER 和 VISUAL-PLAN，再逐图选择原图复用、确定性绘制、生成式解释或混合路线；没有生图能力时仍交付事实台账、确定性图形和提示词包。

### 4. 交互式工艺或数据可视化

输入工艺步骤、指标数据或培训内容。数据量化图优先 Generative UI；需要步骤播放和录屏时转 AI Animation；需要可编辑节点、端口和业务交互时进入 X6 工程路线。所有按钮和控件都必须有真实效果，缺失数据不得补造。

### 5. 科研工艺流程图汇报

输入制造工艺或科研流程文字，先按流程/信息图路由生成可核对的 SVG/HTML/PNG，再追加一份可编辑 PPTX，保留湿基、分流比例、温度段和能耗结论等原始数字；PPTX 首张幻灯片另做渲染回读。

## 质量与验收

推荐顺序：

1. 确认来源、受众、目标格式和编辑要求。
2. 运行 scripts/route_request.py 或按路由手册选择主路由。
3. 先生成可编辑源文件，再导出派生物。
4. 静态 SVG/HTML 图生成后，追加 `emit_editable_pptx.py`，交付 PPTX、报告和 trace。
5. 先做结构/JSON/XML/schema/几何检查，再做浏览器、PPTX 或图片视觉检查。
6. 交付主文件、源文件、派生文件、验证命令和限制说明。

机器验收建议：

~~~powershell
python scripts/route_request.py --text "把这个仓库做成有证据的运行时架构图"
python tests/test_route_request.py
python C:\Users\rabbit\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
~~~

实际发布前还应运行仓库内的 trigger eval、Skill OS conformance、安装模拟和 Test-SkillInstall。它们验证的是不同层面，不能互相替代。

## 安装与验证

推荐使用 Skills CLI 安装：

    npx skills add lhylvsea/lvsea-draw --skill lvsea-draw --yes

你可以这样说：

    用 $lvsea-draw 把这份 Mermaid 流程图美化成适合新员工培训投屏的 SVG，并保留 .mmd 源文件。

发布前检查清单：

- [ ] 路由结果与用户要求的语义、格式和编辑性一致。
- [ ] Mermaid provider 已现场探测，或已明确说明降级原因。
- [ ] 源文件、派生文件和验证报告都能回读。
- [ ] 已运行单元测试、触发评估、Skill 安装检查和敏感信息扫描。

常用验证命令：

    python scripts/route_request.py --text "把这份 Mermaid 图美化并输出 SVG"
    python -m unittest discover -s tests -v

validate_skill.py 属于外部治理工具，不同版本可能带有其维护者自己的 Skill 名称约束；对本仓库应结合 quick_validate.py、触发评估、安装模拟和 Test-SkillInstall.ps1 一起判断，不能把单项失败误写成渲染器失败。

## Troubleshooting

- 如果 Mermaid provider 不可用，保留 .mmd 源文件，并转为 diagram-design 或精确 SVG 路线；不要声称已经生成主题 SVG。
- 如果输出太淡，先指定 github-light、zinc-light、nord-light 或 dracula 等主题，再调整间距、边线对比度和标签长度。
- 如果要求 .drawio、品牌规范或可访问 SVG，格式与交付约束优先于 Mermaid provider，分别转到 drawio-skill 或 diagram-design。

## 来源与许可边界

本 Skill 的方法抽取自用户指定的开源项目和工具页面，来源与固定研究版本记录在 references/source-matrix.md。只借鉴工作流、路由思想、质量门和公开能力边界，不复制上游源码、图片、商标、模板资产或私有数据。lvsea-draw 自身使用 MIT License，具体许可仍以各上游项目原仓库为准。

## 治理依据

本仓库沿用 lvsea-zao-skill 的“来源研究、路由、质量门、证据链”治理思路，并参考 qiaomu-meta-skill 与 yao-meta-skill 的 Skill 组织方式；这些名称是方法来源说明，不代表本仓库自动安装或调用对应工具。

## 已知限制

- AntV Infographic 路由并不意味着本机已安装 `@antv/infographic` 或 `infographic-*` Skill；没有实际运行时只交付结构草案或明确降级产物。
- Pretty Mermaid 路由不等于 provider 已可用；必须现场探测 Node、npm 依赖、主题列表和代表性 `.mmd` 输出。主题渲染成功也不等于事实、语义关系或视觉验收通过。
- drawio-skill 的桌面 CLI、Graphviz、版本和导出能力必须重新探测；当前文档不能替代一次真实导出与图片回读。
- diagram-design 的默认主题不能直接当作品牌交付；品牌项目要先建立或确认 style guide，并保留 style receipt。

- lvsea-draw 本身不会自动安装所有上游工具，也不会凭空创建 MCP 会话。
- 当前机器的本地安装、端口、Node/Python 依赖和浏览器状态必须每次现场探测。
- svg-preview 只能承担预览与人工核对，不是绘图生成器。
- X6 是工程库，不是现成 Agent Skill；只有用户确实要开发图编辑应用时才进入该路线。
- 静态 Skill 检查通过不等于每个外部渲染器、浏览器交互或在线模型已实际调用。
- Skill 已配置 PPTX 伴随流程不等于本次已生成 PPTX；必须以报告中的导出、对象检查和视觉预览状态为准。

## 维护

更新上游路由时，先修改 source-matrix 和 route-playbook，再更新 SKILL.md 的触发边界与回归用例。每次发布前重新运行路由、触发、包结构、安装和远端回读检查。

## License

MIT License。上游项目的许可和版权边界以各自仓库的 LICENSE 为准。
