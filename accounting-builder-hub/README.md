# Accounting Builder Hub

Contributor and maintainer tooling for **claude-for-accounting**: skill design QA, jurisdiction scaffolding, and extension guidance.

This is the maintenance surface — analogous in spirit to a “builder hub” for a legal skill marketplace.

## Who this is for

- People writing new skills or jurisdiction packs
- Firms forking the repo who want a QA checklist before shipping internal skills
- Maintainers reviewing community PRs

## Commands

| Command | Purpose |
|---|---|
| `/accounting-builder-hub:cold-start-interview` | Contributor/maintainer profile (optional) |
| `/accounting-builder-hub:skills-qa` | Evaluate a skill against the Accounting Skill Design Framework |
| `/accounting-builder-hub:jurisdiction-scaffold` | Create a new jurisdiction pack skeleton |

## First principles

1. **Skills are code that touch client money data.** Review them like code.
2. **Show raw SKILL.md** when reviewing — not only a summary.
3. **No install-from-chat of untrusted skills** without human `yes`.
4. **Gates and provenance are non-negotiable** (see `shared/skill-design-framework.md`).

## Related docs

- `../shared/skill-design-framework.md`
- `../shared/jurisdiction-extension-guide.md`
- `../CONTRIBUTING.md`
