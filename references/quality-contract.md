# 统一质量契约

## 海洋哥默认偏好

- 默认中文，先给结论，再给依据和产物。
- 真实来源优先，数字、名称、日期、接口和关系不凭空补齐。
- 产物优先交付可编辑源文件，再给渲染结果和短验证说明。
- 页面和图形偏紧凑、实用、像工作台；避免营销式首屏、卡片堆叠和无效留白。
- 16:9、信息密度高、层级清晰；PPT/单页视觉最低字号原则上不低于 12 pt，HTML/SVG 不使用不可读的小字。
- 制造运营、安全、工艺、党建和党政材料偏庄重、克制、清楚；不要用花哨动效或廉价渐变替代逻辑。
- 用户给出路径、文件名、模板、品牌色或原文时，保留它们，不擅自改名或改口径。

## 内容门

1. 先列出来源文件或 URL。
2. 把事实、用户输入、合理推断和待验证内容分开。
3. 事实关键图中使用真实字段、事件名、接口名、工艺步骤和数据单位。
4. 缺数据时显示待补字段或结构占位，不用虚构数字填满画面。
5. 解释图中的生成式图像只能表达机制隐喻，不能承载精确文本、公式、表格或架构拓扑。

## 结构门

- 每张图只承担一个主要视觉主张。
- 关系必须有方向和语义；颜色不能成为唯一编码。
- 节点多时先分层、分泳道或分阶段；辅助解释放入说明区域而不是继续堆边。
- 对比用并列结构，循环用闭环或回路，层级用树，变化用 Before/Delta/After，数据移动用带标签的流。
- 重要异常、回退、重试、取消和边界必须有显式路径。

## 文件门

| 产物 | 必须保留 |
| --- | --- |
| Archify | JSON IR、HTML、PNG/SVG 或分享卡（按请求） |
| Fireworks | SVG、PNG，动效另留 GIF 和 motion report |
| Draw.io / drawio-skill | .drawio/XML，必要时 PNG/SVG/PDF/PPTX；记录 CLI 与导出状态 |
| Excalidraw | .excalidraw JSON 和渲染图 |
| Drawnix | .drawnix/JSON/PNG 导出文件，不能只留浏览器状态 |
| Technical Explainer | SOURCE-MANIFEST、CLAIM-LEDGER、VISUAL-PLAN、提示词包、图片和 QA |
| Generative UI | 单文件 HTML/SVG/组件代码和数据来源 |
| AntV Infographic | Infographic DSL、模板/主题记录、HTML/SVG，必要时 PNG |
| diagram-design | 自包含 HTML、可访问 SVG、必要时 PNG 和 style receipt |
| X6 | 源码、运行入口、测试和导出样例 |

## 验证门

信息图必须额外检查：模板与主数据族匹配、`title/desc/label/value/icon` 字段完整、语言不被静默翻译、主题颜色可读，以及 DSL 能否在真实运行时解析。编辑图必须额外检查：语义模式没有被装饰替代、节点密度可控、SVG 有 accessible name、品牌 style guide 决策已记录。drawio-skill 需要把 CLI/version/import/export 状态分开记录。

### 确定性检查

- YAML frontmatter、JSON、XML、SVG、HTML 或 TypeScript 语法可读。
- schema、节点 ID、边引用、marker、viewBox、尺寸和路径数据有效。
- 文件能通过 HTTP 或本地读取，输出不是零字节。
- 运行项目自带 validator、build、doctor、check 或最小 CLI 调用。

### 视觉检查

- 浏览器打开 HTML；图片实际渲染后再检查。
- 检查文字越界、裁切、遮挡、箭头穿过无关盒子、标签重叠、图例覆盖、空白失衡和移动端响应式。
- 动画检查至少包含首帧、中间帧、末帧、重复播放或重置状态。
- 无法读取图片时写 visual_review: skipped，不把结构通过写成视觉通过。

### 交付状态

只使用以下明确状态：

- 已实现并验证
- 已配置但未实际调用
- 静态检查通过但交互未验证
- 受外部条件阻塞

不要把这些状态合并为“全部完成”。
