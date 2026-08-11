# lvsea-draw Validation Summary

Date: 2026-08-11

## Static and Routing Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Agent Skills structural validation | PASS | `quick_validate.py .` |
| Yao semantic validation and lint | PASS | `validate_skill.py .`, `lint_skill.py .` |
| Router regression | PASS | 9 unittest cases |
| Trigger evaluation | PASS | 7/7 trigger, 4/4 non-trigger, 2/2 near-neighbor |
| Target compilation | PASS | OpenAI, Claude, Agent Skills, VS Code, generic |
| Conformance suite | PASS | 5/5 targets |
| Trust scan | PASS | 0 secrets; 1/1 CLI help smoke; no network/file-write/subprocess/interactive script capability |

## Package Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Cross-platform package | PASS | 4 adapters and 97 safe archive entries |
| Package verification | PASS | `reports/package_verification.json` |
| Install simulation | PASS | `reports/install_simulation.json` |
| Registry audit | PASS | `reports/registry_audit.json` |
| Runtime permission probe | PASS | 4/4 adapters; metadata fallback explicit; no native enforcement claimed |

## Minimal Real Calls

- The bundled router emitted a valid route for an evidence-first runtime architecture request: primary `evidence-architecture`, executor `$archify`, secondary `precise-technical-graphic`.
- The installed Archify CLI was probed against its actual command surface. Its assumed `doctor` and `guide` commands do not exist; the corrected `examples`, `inspect`, `validate`, `render`, and `check` path passed on the cache-miss sequence example and produced `work/archify-smoke.html` outside this package.

## Capability State

- Configured and referenced: Archify, Fireworks Tech Graph, bruce-drawio, Drawnix, Excalidraw Diagram, Technical Explainer Illustrator, Generative UI MCP, AI Animation, Understand Anything, and X6 engineering route.
- Not claimed as live calls in this validation: Draw.io MCP, Generative UI MCP server, Drawnix browser session, Kami, X6 app runtime, external image-generation API, or browser visual inspection.
- The package is a router and quality bus; downstream tools remain separately installed and are probed at task time.
