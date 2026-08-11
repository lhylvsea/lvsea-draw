# Compiled Targets

- OK: `True`
- Targets: `1`
- Pass: `1`
- Warn: `0`
- Block: `0`

## Target Transforms

| Target | Status | Native Surface | Adapter Mode | Permissions | Degradation | Generated Files |
| --- | --- | --- | --- | --- | --- | --- |
| `vscode` | `pass` | VS Code/Copilot Agent Skills project or user scope | `vscode-agent-skills-adapter` | `none` | `agent-skills-source-with-vscode-notes` | targets/vscode/adapter.json, targets/vscode/README.md |

## Native Behavior Contracts

### vscode

- Native surface: VS Code/Copilot Agent Skills project or user scope
- Activation: Use folder name plus SKILL.md name/description; keep description under platform limits.
- Resources: Install as project or user scoped skill source, preserving relative references and scripts.
- Scripts: Scripts require workspace trust and operator/client approval outside this compiler.
- Permission enforcement: `client-or-workspace-trust`; native enforcement `False`
- Review artifacts: SKILL.md, agents/interface.yaml, reports/review-studio.html


## Failures

- None

## Warnings

- None
