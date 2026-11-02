# Package Verification

- OK: `True`
- Package directory: `C:\Users\rabbit\.codex\skills\lvsea-draw\dist`
- Targets: `4 / 4` adapters present
- Archive present: `True`
- Archive SHA256: `3124289e96ba489b00519c808444c9bf0ff6b61131d320c5b03f4608adcaa961`
- Nested SKILL.md entries: `0`
- Failures: `0`
- Warnings: `0`

## Checks

| Check | Status | Detail |
| --- | --- | --- |
| `package-manifest` | `pass` | Package manifest exists: C:\Users\rabbit\.codex\skills\lvsea-draw\dist\manifest.json |
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
