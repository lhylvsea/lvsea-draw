# 本机适配器与能力边界

本文件是 2026-08-11 在当前 Windows 主机上做的发现快照。路径、端口、依赖、浏览器会话和 MCP 状态都可能变化；每次实际任务必须重新探测。

| 能力 | 本机发现 | 使用时必须再核对 |
| --- | --- | --- |
| Archify | C:\Users\rabbit\.codex\skills\archify、C:\Users\rabbit\.agents\skills\archify | node 版本、bin/archify.mjs doctor、目标模式和输出目录 |
| Drawnix | C:\Users\rabbit\.codex\skills\drawnix；Skill 记录的应用路径是 C:\Users\rabbit\apps\drawnix | 7200 端口、服务进程、真实导出文件和浏览器读取 |
| Generative UI | C:\Users\rabbit\.codex\skills\generative-ui-mcp | 当前是规则内嵌 Skill，不代表 generative-ui MCP 已注册 |
| Technical Explainer | C:\Users\rabbit\.codex\skills\technical-explainer-illustrator | Python 脚本、图片生成能力和实际渲染器 |
| Fireworks | C:\Users\rabbit\.agents\skills\fireworks-tech-graph | cairosvg 或 rsvg-convert、FFmpeg/FFprobe、Chrome/Chromium |
| Excalidraw | C:\Users\rabbit\.agents\skills\excalidraw-diagram-skill | renderer、Node 依赖和实际图片查看能力 |
| Understand Anything | C:\Users\rabbit\.agents\skills\understand 及 understand-* 子 Skill | 项目是否有 .ua 或 .understand-anything 图谱、图谱 commit 是否新鲜 |
| Draw.io | C:\Users\rabbit\.agents\skills\drawio，frontmatter 调用名是 bruce-drawio | 本地桌面版、浏览器、MCP 或仅 XML 生成能力 |
| AI Animation | C:\Users\rabbit\.agents\skills\AI-Animation-Skill，入口 frontmatter 为 science-content-ppt | 模板文件、浏览器截图和动画重置脚本 |
| Kami | 本次未发现 C:\Users\rabbit\.codex\skills\kami 或 C:\Users\rabbit\.agents\skills\kami 直接入口 | 使用前先发现；缺失时转 bentohttp-ppt、codex-slides 或其他文档 Skill |
| X6 | 只研究了 AntV/X6 源码仓库，本机未将它作为现成 Agent Skill | package manager、React/Vue 工程、SSR 和浏览器测试 |
| SVG Preview | 只确认了在线预览页面，不将其当本地生成能力 | 网络、隐私、SVG 是否包含敏感内容 |

## 探测原则

1. 先检查本机已安装入口和技能 frontmatter。
2. 再检查命令、依赖、端口和可读取的最小输出。
3. MCP 必须实际读取注册状态或完成最小调用，不能仅凭配置文件。
4. 只有在真实调用和结果回读后，才把状态升级为已实现并验证。
5. 任何路径或版本写入最终报告时，都标记为本次运行快照。
