# 可编辑 PPTX 伴随产物

## 目标

这是一条后处理路线，不替代 Archify、Fireworks、diagram-design、Infographic 或 Draw.io 的主图源：

`canonical SVG / static HTML` → `SVG compatibility normalization` → `PPT Master quality gate` → `native DrawingML PPTX` → `package/object inspection` → `optional visual readback`

默认原则是“源文件不动、派生物新增”。因此 JSON、HTML、SVG、PNG、Draw.io/XML、事实台账和其他原路由产物必须继续保留，PPTX 只是新增的汇报交付物。

## 何时必须生成

- 主路由产生 `ppt-ready.svg`、独立 SVG 或包含内联 SVG 的静态 HTML。
- 用户说“可编辑 PPTX”“SVG 转 PPTX”“用于科研 PPT”“每次输出都附一份 PPTX”时，伴随产物是硬性要求。
- 动态 HTML、Canvas、WebGL 或图片组不能直接声称可以转换；必须先得到可验证的静态 SVG，或报告 `blocked` / `missing capability`。

## 标准命令

```powershell
python scripts/emit_editable_pptx.py path/to/diagram.svg `
  -o output/diagram-可编辑.pptx `
  --render-preview
```

HTML 输入也可以直接交给适配器，但只会提取第一个静态 `<svg>`：

```powershell
python scripts/emit_editable_pptx.py path/to/diagram.html `
  -o output/diagram-可编辑.pptx
```

需要固定 PPT Master 安装位置时使用 `--ppt-master-dir`，或设置 `PPT_MASTER_SKILL_DIR`。适配器默认探测：

- `%USERPROFILE%\.codex\skills\ppt-master`
- `%USERPROFILE%\.agents\skills\ppt-master`

## 适配动作

适配器只做为导出所需的最小归一化：

1. 解析并校验 SVG 根节点、`viewBox` 和 16:9 画布。
2. 将简单 CSS class、inline style 写入元素属性。
3. 移除 PPT Master 当前不接受的 `<filter>` 和 `filter` 属性。
4. 将箭头 marker 按线条颜色匹配；遇到颜色不一致时复制并重着色 marker，不改原始 SVG。
5. 创建临时 `svg_output/slide_01.svg` 和 `spec_lock.md`，以 `--pptx-structure flat` 导出。

## 交付契约

```text
<主图源>                         保留
<主图源>-可编辑.pptx              必须新增
<主图源>-可编辑-svg-quality.json   结构/版式质量结果
<主图源>-可编辑.trace.json         转换决策轨迹（若 PPT Master 生成）
<主图源>-可编辑.report.json        汇总状态、限制和实际路径
<主图源>-可编辑-preview.png        仅在请求渲染预览且工具可用时生成
```

PPTX 报告至少区分：

- `passed`：导出、PPTX 包和对象检查通过，且无适配器警告。
- `passed-with-warnings`：导出和阻塞门通过，但存在字体、单位、图片或未做视觉预览等提示。
- `blocked`：PPT Master 缺失、质量门失败、导出失败或源图无法解析。

“可编辑”只表示 PPT Master 支持的 SVG 文本和几何对象写成了原生 DrawingML；嵌入图片、SVG 外部资源、动态 HTML 状态和不支持的 CSS 效果不能被包装成可编辑文本或图形。

## 验收清单

1. 源 SVG/XML 可读，`viewBox`、marker 和文字存在。
2. `svg_quality_checker.py` 无 blocking error；advisory warning 必须进入报告。
3. `svg_to_pptx.py` 成功，PPTX 非零字节且 ZIP 完整。
4. PPTX 至少有一页；记录原生 shape、文本、图片和 media 数量。
5. 有条件时用 LibreOffice/Poppler 或 PowerPoint 实际渲染首张幻灯片并回读；未执行时写明 `visual_preview: not-requested/skipped`。
6. 不能因 PPTX 失败而删除或覆盖主图源。
