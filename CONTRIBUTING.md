# Contributing to Claude for Accounting

Notes for anyone writing or editing a plugin in this repo. Keep this practical — design principles that protect output quality, not a style guide.

## Before your first PR

1. Read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
2. Sign the [CLA](./CLA.md) when the bot asks (or affirm in the PR).
3. Run `python3 scripts/validate_marketplace.py` and fix failures.
4. Read `shared/skill-design-framework.md` and `shared/guardrails.md`.

## Design principle: SKILL.md encodes the right behavior; CLAUDE.md is the net

Every plugin ships two layers:

1. **`<plugin>/skills/<skill>/SKILL.md`** — what this skill does, step by step. Narrow, task-specific.
2. **`<plugin>/CLAUDE.md` + `shared/guardrails.md`** — firm profile template + safety net (number integrity, gates, headers).

**If a skill’s correct output depends on a guardrail catching a mistake the SKILL.md would have made, that’s a design smell.** Put the behavior in the skill. The guardrail stays (belt and suspenders).

### Accounting-specific rules of thumb

- **Doctrine in the skill.** If the skill covers year-end adjustments, include the full adjustment catalogue checklist — not “also consider accruals.”
- **Provenance on numbers, not paragraphs.** Tag the digit: `[source: bank statement May 2025 p.3]` or `[model calculation — verify]`. Tags on surrounding prose get lost.
- **Hard gates default-on.** “Do not proceed to FS if TB does not balance” is a gate heading, not a parenthetical.
- **Never invent statutory rates or due dates.** Point at jurisdiction reference files; mark `[verify — authoritative source]` when training data may lag.
- **Jurisdiction is a pack, not a fork.** New country → `references/jurisdictions/<id>/` + guide in `shared/jurisdiction-extension-guide.md`. Do not copy the entire marketplace.

## Where to put changes

| Change | Location |
|---|---|
| Stage workflow steps | Relevant `skills/*/SKILL.md` |
| Firm-neutral defaults | Plugin `CLAUDE.md` template only (placeholders) |
| Malaysia standards/tax | `references/jurisdictions/malaysia/` **and** keep root shims updated if present |
| New country | New folder under `references/jurisdictions/` + builder-hub scaffold |
| Note wording | `references/notes-templates/` |
| Entity COA | `references/coa_templates/coa_*.json` |
| Industry overlay | `references/coa_templates/industry/*.json` |
| Shared safety | `shared/guardrails.md` |
| Marketplace registry | `.claude-plugin/marketplace.json` |
| Validators | `scripts/validate_marketplace.py` |

## Versioning

- **Patch** (`1.1.x`) — wording, bugfixes, reference updates that don’t change skill contracts.
- **Minor** (`1.x.0`) — new skills, new required inputs, new jurisdiction packs.
- **Major** — pipeline stage renames or breaking config path changes (avoid).

Bump the affected plugin’s `.claude-plugin/plugin.json` `version` on material change. Update [CHANGELOG.md](./CHANGELOG.md).

## PR checklist

- [ ] `python3 scripts/validate_marketplace.py` passes
- [ ] SKILL.md frontmatter `name` + `description` accurate for auto-invocation
- [ ] No hard-coded firm names, personal emails, or client data
- [ ] No fabricated sample financial figures presented as real
- [ ] Load-bearing numbers instruct source provenance
- [ ] New references linked from the skill that needs them
- [ ] CHANGELOG entry under Unreleased or version section
- [ ] Plugin README updated if commands changed

## What we will not merge

- Skills that encourage fabricating balances “to make it work”
- Removal of mathematical blockers without an equivalent harder gate
- Jurisdiction content claimed as official without a “workflow summary / verify” banner
- Secrets, API keys, or live client working papers

## Local validation

```bash
python3 scripts/validate_marketplace.py
python3 scripts/validate_marketplace.py --strict
```

## Questions

Open a GitHub Discussion or Issue with the `question` label. For security reports, see [SECURITY.md](./SECURITY.md).
