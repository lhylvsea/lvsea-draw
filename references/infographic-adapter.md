# Infographic 适配契约

本文件是 `infographic-composition` 路由的本地适配层，不是 AntV Infographic 源码或模板的镜像。它把上游能力转成可验证的输入、输出和降级状态。

## Provider 状态

交付时必须把以下状态分开写：

- **已实际调用**：本机找到 `@antv/infographic` 或 `infographic-*` Skill，完成 DSL 解析、HTML/SVG 渲染和结果回读。
- **已配置但未实际调用**：只找到文档、Skill 入口或网络 CDN，没有完成本次渲染。
- **降级执行**：保留信息结构和内容台账，改由 `diagram-design` 或 `precise-technical-graphic` 生成可验证的 HTML/SVG/PNG。
- **阻塞**：模板、运行时、字体、图标或用户数据缺失，不能安全补齐。

上游还拆分了 `infographic-creator`、`infographic-syntax-creator`、`infographic-structure-creator`、`infographic-item-creator` 和 `infographic-template-updater`。在 lvsea-draw 中，前两个属于内容/DSL 生成能力；后三个只在明确要修改 Infographic 框架源码、结构组件、Item 组件或模板目录时才触发，不用于普通信息图交付。

## 结构化流程

1. 锁定受众、语言、尺寸、输出格式和信息来源；数据、单位、时间和关系进入事实台账。
2. 先判断结构族：严格步骤用 `sequence-*`，并列要点用 `list-*`，两方/多方比较用 `compare-*`，层级用 `hierarchy-*`，节点关系用 `relation-*`，数值趋势用 `chart-*`。
3. 为模板选择唯一的主数据族，例如 `sequences`、`lists`、`compares`、`root`、`nodes + relations` 或 `values`；不把互不兼容的族硬塞进同一张图。
4. 保持用户输入语言；语义数据项优先补充稳定的 `icon`，数值单位放在标签或说明中，不把单位混入数值字段。
5. 保存 Infographic DSL、模板名、主题、事实来源和渲染状态，再生成 HTML/SVG；如需离线交付，优先使用本地包，不默认依赖 CDN。
6. 完成语法/结构检查后，打开 HTML 或读取导出的 SVG/PNG，检查文字容量、viewBox、图标、颜色对比、移动端裁切和空白平衡。

## 降级规则

- 没有真实 AntV 运行时：不伪造 Infographic SVG；把 DSL 作为结构草案，并用 `editorial-diagram` 或 `precise-technical-graphic` 生成可验证产物。
- 需要品牌规范或可访问静态图：将信息结构交给 `editorial-diagram`，建立/确认 style guide，并保留 style receipt。
- 需要真实控件、筛选、播放或数据联动：转 `interactive-widget`；不要把静态 SVG 的 hover 伪装成完整交互。
- 需要 `.drawio` 编辑：转 `editable-drawio`；Infographic DSL 只能作为内容结构参考，不替代 Draw.io XML。

## 最小交付清单

- `source.infographic` 或等价 DSL 文件；
- 模板、主数据族、语言、主题和来源记录；
- HTML/SVG/PNG 派生物及实际渲染状态；
- 结构检查、浏览器/图片回读和未验证能力清单；
- 若发生降级，记录原路由、替代路由、原因和仍存在的风险。
