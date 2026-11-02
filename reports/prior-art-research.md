# Prior-art research: Pretty Mermaid integration

## Source boundary

- Source repository: <https://github.com/imxv/Pretty-mermaid-skills>
- Read: upstream `README.md`, `README_CN.md`, root `SKILL.md`, `LICENSE`, `package.json`, `references/THEMES.md`, `references/DIAGRAM_TYPES.md`, `references/api_reference.md`, and the bundled rendering scripts.
- Research snapshot: commit `e234ab73c2992f03c36db04fd55ebb90abca9c45`, read on 2026-11-01.
- License evidence: upstream repository exposes an MIT license; lvsea-draw does not copy upstream code, examples, theme gallery, or npm runtime.
- Not claimed: browser, MCP, external model, human blind review, or brand-specific output quality.

## Extracted mechanisms

1. Keep Mermaid source as the durable input and render SVG, PNG, or terminal text as derived artifacts.
2. Choose a named theme or explicit color roles instead of relying on a bare default.
3. Tune padding and graph spacing before shrinking labels.
4. Use batch rendering when multiple `.mmd` files need a consistent theme.
5. Validate syntax/render exit, non-empty output, format signatures, and visual fit for long labels/CJK.

## Synthesis decision

The mechanisms are adapted into `mermaid-polish`, an lvsea-draw route and adapter contract. Explicit `.drawio`/XML and brand/accessibility requirements retain precedence. Provider absence or unsupported syntax produces a transparent fallback, not a fabricated Pretty Mermaid result.
