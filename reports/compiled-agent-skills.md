# Compiled Targets

- OK: `True`
- Targets: `1`
- Pass: `1`
- Warn: `0`
- Block: `0`

## Target Transforms

| Target | Status | Native Surface | Adapter Mode | Permissions | Degradation | Generated Files |
| --- | --- | --- | --- | --- | --- | --- |
| `agent-skills` | `pass` | Agent Skills standard source tree | `neutral-agent-skills-source` | `none` | `neutral-source` | SKILL.md, agents/interface.yaml |

## Native Behavior Contracts

### agent-skills

- Native surface: Agent Skills standard source tree
- Activation: Use SKILL.md frontmatter name and description for progressive disclosure.
- Resources: Keep optional directories as relative resources next to SKILL.md.
- Scripts: Scripts remain local optional resources and should advertise --help when executable.
- Permission enforcement: `consumer-enforced-or-metadata-only`; native enforcement `False`
- Review artifacts: SKILL.md, agents/interface.yaml, reports/review-studio.html


## Failures

- None

## Warnings

- None
