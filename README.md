# Skill Builder

A portable Agent Skills authoring workspace.

## Included

- `skills/skill-builder/`: the Skill Builder Agent skill.
- `templates/SKILL_TEMPLATE.md`: a starter template for new skills.
- `skills/skill-builder/scripts/validate_skill.py`: a dependency-free basic validator.
- `tests/test-cases.md`: evaluation scenarios.

## Portability

The core follows the open Agent Skills folder format: a skill directory with a `SKILL.md` file containing YAML frontmatter (`name` and `description`) and Markdown instructions. Optional scripts, references, and assets are kept alongside it.

A compatible host must implement skill discovery/loading. Platform-specific integrations and tool permissions are not supplied by this repository.

## Validate

Run:

```bash
python skills/skill-builder/scripts/validate_skill.py skills/skill-builder
```

For full specification validation, install and run the official `skills-ref` validator when available:

```bash
skills-ref validate skills/skill-builder
```

## Development status

Initial v1 scaffold. Review platform-specific installation instructions before deploying to any particular agent.
