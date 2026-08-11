# Package Verification

- OK: `True`
- Package directory: `C:\Users\rabbit\Documents\Codex\2026-08-11\skill-agent-goal-boss-draw-qiaomu-2\outputs\lvsea-draw\dist`
- Targets: `4 / 4` adapters present
- Archive present: `True`
- Archive SHA256: `1e2845bb6257076f8debed183909c90490c8efb03c5f55fb81eb3f02d3875bb8`
- Nested SKILL.md entries: `0`
- Failures: `0`
- Warnings: `0`

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `package-manifest` | `pass` | Package manifest exists: C:\Users\rabbit\Documents\Codex\2026-08-11\skill-agent-goal-boss-draw-qiaomu-2\outputs\lvsea-draw\dist\manifest.json |
| `claude-adapter` | `pass` | Adapter exists for target: claude |
| `generic-adapter` | `pass` | Adapter exists for target: generic |
| `openai-adapter` | `pass` | Adapter exists for target: openai |
| `vscode-adapter` | `pass` | Adapter exists for target: vscode |
| `archive-safe-paths` | `pass` | Archive has no absolute or parent-traversal entries |
| `archive-entry-lvsea-draw/SKILL.md` | `pass` | Archive contains lvsea-draw/SKILL.md |
| `archive-entry-lvsea-draw/manifest.json` | `pass` | Archive contains lvsea-draw/manifest.json |
| `archive-entry-lvsea-draw/agents/interface.yaml` | `pass` | Archive contains lvsea-draw/agents/interface.yaml |
| `archive-single-skill-entrypoint` | `pass` | Archive exposes only the root SKILL.md entrypoint |
| `archive-excludes-generated` | `pass` | Archive excludes generated dist/, .previews/, and tests/tmp* contents |
| `registry-ok` | `pass` | Registry audit is OK |
| `registry-name-match` | `pass` | Registry package name matches package manifest |
| `registry-version-match` | `pass` | Registry package version matches package manifest |
| `registry-compat-claude` | `pass` | Registry compatibility is reviewable for target: claude |
| `registry-compat-generic` | `pass` | Registry compatibility is reviewable for target: generic |
| `registry-compat-openai` | `pass` | Registry compatibility is reviewable for target: openai |
| `registry-compat-vscode` | `pass` | Registry compatibility is reviewable for target: vscode |

## Failures

- None

## Warnings

- None
