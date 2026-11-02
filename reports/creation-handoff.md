# Creation handoff: lvsea-draw 0.4.0

## Goal

Integrate Mermaid rendering and visual polish into the existing Draw router without turning lvsea-draw into a copied Mermaid renderer. Preserve the local v0.3.0 PPTX companion capability while bringing the GitHub repository up to the same package revision.

## Source and ownership

- Current runtime baseline: local `lvsea-draw` v0.3.0.
- Remote baseline: `lhylvsea/lvsea-draw` main at `d53ddae`.
- New route: `mermaid-polish` with executor `pretty-mermaid`.
- Public package remains owned by `lvsea`; the upstream Pretty Mermaid project remains its own provider.

## keep / adapt / reject / invent

- **keep**: `.mmd` source preservation, named themes, explicit color roles, SVG/PNG/ASCII outputs, batch rendering, spacing controls, and output readback.
- **adapt**: route precedence, theme selection by audience and surface, Chinese trigger language, provider policy, and the existing static-SVG-to-editable-PPTX companion contract.
- **reject**: copied upstream scripts/assets/runtime, silent npm installation, source overwrite, and claims that a renderer pass proves semantic or visual correctness.
- **invent**: the `mermaid-polish` route, brand/accessibility and Draw.io precedence gates, theme receipt requirements, and transparent fallback status.

## Verification boundary

- Router unit tests: passed, 19 total tests after the Mermaid regression cases were added.
- Lvsea governed trigger evaluation: passed, 22/22 cases across positive, negative, near-neighbor, and adversarial buckets.
- Skill IR and context budget reports: regenerated for v0.4.0.
- Pretty Mermaid provider: actual local smoke test passed for 15 themes, six example diagrams, SVG/PNG/ASCII CLI output, custom colors, and interactive XY coverage; representative SVG/PNG/ASCII files were non-empty.
- Still separate: human visual approval, browser/OS-level interaction, brand approval, and downstream PPTX output for a user-specific diagram.

## Release boundary

The change is prepared on a feature branch. Remote publication must use the branch/PR/release path, and local installation is synchronized only after the final committed tree is selected.
