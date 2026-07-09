# Contributing to Claude for Accounting

Notes for anyone writing or editing a plugin in this repo. Keep this practical — design principles that protect output quality, not a style guide.

## Before your first PR

1. Read [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
2. Sign the [CLA](./CLA.md) when the bot asks (or affirm in the PR).
3. Read `shared/skill-craft.md`, `shared/skill-design-framework.md`, `CONTEXT.md`, `shared/guardrails.md`, `shared/architecture.md`.
4. Run the full check suite (must pass):

```bash
pip install -r requirements.txt   # once
bash scripts/ci_check.sh
# if you edit modular skills:
python3 scripts/sync_umbrella.py
python3 scripts/sync_umbrella.py --check
```

Do not open a PR with failing `ci_check` or out-of-date umbrella skills.

## Design principle: SKILL.md encodes the right behavior; CLAUDE.md is the net

Every plugin ships two layers:

1. **`<plugin>/skills/<skill>/SKILL.md`** — what this skill does, step by step. Narrow, task-specific.
2. **`<plugin>/CLAUDE.md` + `shared/guardrails.md`** — firm profile template + safety net (number integrity, gates, headers).

**If a skill’s correct output depends on a guardrail catching a mistake the SKILL.md would have made, that’s a design smell.** Put the behavior in the skill. The guardrail stays (belt and suspenders).

Craft (how to write skills so agents behave the same *way* every run) lives in **`shared/skill-craft.md`** — invocation, description load, completion criteria, progressive disclosure, pruning. Accounting gates live in **`shared/skill-design-framework.md`**. Domain words live in **`CONTEXT.md`**.

### Accounting-specific rules of thumb

- **Doctrine in the skill.** If the skill covers year-end adjustments, include the full adjustment catalogue checklist — not “also consider accruals.” Disclose long catalogues behind a strong pointer if needed.
- **Completion criteria.** Every step ends with a checkable done condition (and exhaustive bars where material).
- **Invocation deliberate.** Stage skills are usually model-invoked; builder skills (`skills-qa`, jurisdiction-scaffold, builder cold-start) set `disable-model-invocation: true`.
- **Lean descriptions.** Front-load the verb; one trigger branch; no essay of the whole skill in frontmatter.
- **Provenance on numbers, not paragraphs.** Tag the digit: `[source: bank statement May 2025 p.3]` or `[model calculation — verify]`. Tags on surrounding prose get lost.
- **Hard gates default-on.** Prefer positive procedure (`roll_tb` only) paired with blocker behaviour.
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
| Validators / CI | `scripts/validate_marketplace.py`, `scripts/ci_check.sh` |
| Beancount / Fava | `beancount-ledger/`, `scripts/export_to_beancount.py` |
| Bank PDF adapters | `scripts/extract_maybank_islamic_pdf.py`, `references/bank_statement_extraction.md` |
| Excel generation | `shared/excel_deliverables.md`, `scripts/generate_workbook.py` (openpyxl) |

## Versioning

This project is at **0.0.x** (early public scaffold). Until 1.0:

- **Patch** (`0.0.x`) — fixes, docs, non-breaking skill wording, new optional adapters  
- **Minor after 1.0** — new skills / required inputs  
- **Major** — pipeline renames or config path breaks (avoid)

Bump affected plugin `version` fields together with root `VERSION` and [CHANGELOG.md](./CHANGELOG.md).

## PR checklist

- [ ] `python3 scripts/validate_marketplace.py` passes
- [ ] SKILL.md frontmatter `name` + `description` craft-worthy (lean triggers; user-invoked if builder)
- [ ] Steps have completion criteria (or pure-reference exhaustive bar)
- [ ] Intent placed on `shared/skill-collapse-map.md` if new stage surface
- [ ] No hard-coded firm names, personal emails, or client data
- [ ] No fabricated sample financial figures presented as real
- [ ] Load-bearing numbers instruct source provenance
- [ ] New references linked from the skill that needs them
- [ ] CHANGELOG entry under Unreleased or version section
- [ ] Plugin README updated if commands changed
- [ ] `/accounting-builder-hub:skills-qa` green for new/edited number skills

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
