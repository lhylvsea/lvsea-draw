# lvsea-draw 中文使用说明

> 本文件为 lvsea-draw 的中文补充层。技能正文以同目录 SKILL.md 为准。

## 一、触发条件 / 调用方式
当用户需要用 lvsea-draw 相关能力处理任务时调用本技能。新增 Mermaid 触发边界包括：“Mermaid 已经画出来但太寡淡”“换 Mermaid 主题/配色”“把 Mermaid 渲染成 SVG/PNG/ASCII”“批量美化 `.mmd`”。这类请求进入 `mermaid-polish`，优先使用本机 `pretty-mermaid` provider；明确要品牌规范、可访问 HTML/SVG 或 `.drawio` 时，格式路由优先。

典型触发表达（示例）：
- “帮我用 lvsea-draw 处理这个任务”
- “我需要 lvsea-draw 相关的能力”
- 用户在对话中描述的需求与 lvsea-draw 的能力范围匹配时。

## 二、典型应用场景
1. 场景一：用户提出与 lvsea-draw 核心能力直接相关的请求。
2. 场景二：用户希望自动化或规范化完成某类重复性工作。
3. 场景三：用户需要参考 lvsea-draw 提供的方法论、模板或工作流。
4. 场景四：多步骤任务中，某一步骤属于 lvsea-draw 的职责范围。

### Mermaid 美化调用示例

```text
用 $lvsea-draw 把这段 Mermaid 保留为 .mmd，换成适合培训投屏的主题，输出 SVG 和 PNG，并检查长标签是否被裁切。
```

```text
Mermaid 已经能渲染，但颜色太淡、边线不清，请用 mermaid-polish 选择高对比度主题，同时保留原始源码。
```

```text
把 diagrams 目录里的 Mermaid 批量输出为 GitHub 深色 SVG 和终端 ASCII，记录主题、字体和间距参数。
```

```text
按品牌规范把 Mermaid 重绘成可访问的自包含 HTML，并另外保留一份主题化 SVG。
```

## 三、使用说明 / 推荐工作流程
1. 先确认用户真实目标与验收标准。
2. 读取 SKILL.md 正文与同目录参考文件，理解本技能的方法与约束。
3. 按技能定义的工作流逐步执行，每步给出可验证判据。
4. 交付前用证据（命令输出 / 测试结果）闭环，不把“看起来完成”当作完成。

## 四、注意事项与边界
- 仅在 lvsea-draw 定义的能力范围内使用，不超出范围自行发挥。
- 涉及外部命令、API、网络或依赖时，先确认来源可信与权限。
- 不可逆操作（删除 / 覆盖 / 发布 / force push 等）须先明确确认。
- 不将密钥、凭据写入产物或日志；发现泄露立即报告并停止。
- 验收未通过或证据不足时，不得声称任务完成。
- Pretty Mermaid 需要 Node.js 16+ 及其 npm 依赖；不要依赖脚本的静默联网安装。provider 缺失或语法不支持时，保留 `.mmd`，明确降级到 diagram-design、精确 SVG 或 Draw.io。
- 主题只是表现层，不能替代事实来源、节点关系、异常分支和责任边界；SVG/PNG 生成成功后仍要做文本、箭头、间距和视觉回读。
