# Pretty Mermaid 适配器

## 适用范围

当 Mermaid 已经能生成图，但出现“太素、太寡淡、主题不统一、边和文字不够清楚”时，使用 `mermaid-polish` 作为渲染与美化路由。它是渲染层，不替代事实核对、关系建模或用户指定的可编辑格式。

研究来源：<https://github.com/imxv/Pretty-mermaid-skills>

研究快照：`e234ab73c2992f03c36db04fd55ebb90abca9c45`（2026-11-01 本地只读审阅）。上游许可证为 MIT，运行要求 Node.js 16+。

## 机制取舍

| 决策 | 采用方式 |
| --- | --- |
| keep | 保留 `.mmd` 作为 canonical source；保留 SVG、PNG、ASCII/Unicode 三类输出；保留 15 个命名主题、显式颜色角色、批量渲染和六类 Mermaid 图支持。 |
| adapt | 将上游“主题选择 + 渲染 + 回读”纳入 lvsea-draw 的 `mermaid-polish` 路由；把主题、字体、padding、node spacing、layer spacing 和 component spacing 记录到交付 manifest；与品牌图、Draw.io 和 PPTX 伴随路由分离。 |
| reject | 不把上游脚本、`beautiful-mermaid` 运行时代码、主题图库、示例图或 npm 依赖复制进 lvsea-draw；不依赖浏览器渲染；不接受静默联网安装、静默覆盖用户源文件或把“命令成功”当成视觉通过。 |
| invent | 建立格式优先和品牌/可访问性优先的路由门；为打印、GitHub、开发工具、终端和高对比度场景给出主题默认值；所有失败都保留 `.mmd` 并明确降级到 `editorial-diagram`、`precise-technical-graphic` 或 `editable-drawio`。 |

## 路由规则

1. 用户明确要求 `.drawio`、XML 或继续编辑：`editable-drawio` 优先，Mermaid 只作为输入转换或协作路由。
2. 用户明确要求品牌规范、可访问 SVG 或自包含 HTML：`editorial-diagram` 优先，`mermaid-polish` 负责可选的 Mermaid 样式起点或回退渲染。
3. 用户提供 `.mmd`，或说 Mermaid 已能画出但太寡淡、要换主题/配色/渲染：`mermaid-polish` 优先。
4. Mermaid 语法超出 provider 支持范围，或需要工程级几何/动画：保留 `.mmd`，转 `precise-technical-graphic` 或 `editable-drawio`，不得伪造 Pretty Mermaid 成功。

## 主题策略

主题不是装饰，必须与受众和载体匹配：

- 打印、正式报告：`zinc-light` 或 `github-light`。
- GitHub/浅色文档：`github-light`；深色文档：`github-dark`。
- 开发工具或终端：`tokyo-night`、`zinc-dark` 或 `one-dark`。
- 高对比度演示：`dracula`，同时检查长标签和边线对比度。
- 冷静的企业技术图：`nord` 或 `nord-light`。

品牌项目不得直接把内置主题当作品牌交付；需要记录 style guide、色值角色和确认状态。颜色不能成为唯一语义编码，异常、分支、状态和责任仍需通过形状、标签和方向表达。

## 标准调用

在已安装的 `pretty-mermaid` provider 根目录执行，源文件和输出写入用户指定目录：

```bash
node scripts/render.mjs --input diagram.mmd --output diagram.svg --theme tokyo-night
node scripts/render.mjs --input diagram.mmd --output diagram.png --format png --width 1200 --theme github-light
node scripts/render.mjs --input diagram.mmd --output diagram.txt --format ascii --color-mode none
node scripts/batch.mjs --input-dir diagrams --output-dir rendered --format svg --theme github-dark --workers 4
```

颜色明确时使用 `--bg`、`--fg`、`--line`、`--accent`、`--muted`、`--surface`、`--border`，布局拥挤时优先调整 `--padding`、`--node-spacing`、`--layer-spacing` 和 `--component-spacing`，不要先缩小文字。

## 验收与交付

至少返回：

- 原始 `.mmd`，不得只交付图片；
- 渲染输出及格式、主题、字体、颜色和间距记录；
- 命令退出状态、文件非空、SVG 根节点/viewBox 或 PNG 文件头检查；
- 长标签、CJK、箭头、边标签、分支、断开组件和拥挤布局的视觉回读；
- provider 缺失、语法不支持、PNG 转换失败或视觉不通过时的 `missing_capabilities`、`fallback_used` 和 `remaining_risks`。

如果输出 canonical SVG 或静态 HTML，继续执行 lvsea-draw 的 `scripts/emit_editable_pptx.py` 伴随流程；PPTX 不是 Mermaid 源文件的替代品。

## 能力边界

上游 README 声称支持 Flowchart、Sequence、State、Class、ER、XY Chart，15 个主题以及 SVG/PNG/ASCII 输出；本适配器只把这些作为已研究能力，不把本机运行时、字体、Node 依赖或视觉回读状态写成默认已验证。实际交付前必须现场探测 provider 并按本文件的最小调用验证。
