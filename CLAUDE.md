# Claude for Accounting — Repo Guide for Agents

This repository is an **open-source Claude Code / Cowork plugin marketplace** for accounting engagements, structured like [claude-for-legal](https://github.com/anthropics/claude-for-legal): stage plugins, granular skills, firm practice profiles, jurisdiction packs, and shared guardrails.

## When working in this repo

1. Read `shared/guardrails.md` before changing skills that produce numbers.
2. Read `CONTRIBUTING.md` and `shared/skill-design-framework.md` before new skills.
3. Prefer jurisdiction packs over hard-coding country rules into stage skills.
4. Never commit client data, secrets, or hard-coded firm branding.
5. Run `python3 scripts/validate_marketplace.py` after structural edits.

## Plugin map → engagement pipeline

| Stage | Plugin |
|---|---|
| Firm + engagement setup | `engagement-accounting` |
| Record & classify | `bookkeeping-accounting` |
| Reconcile + preliminary TB | `reconciliation-accounting` |
| Year-end + ATB | `year-end-accounting` |
| Standards review | `mpers-accounting` (name historical; content is standards pack + review) |
| Statements + notes | `financial-statements-accounting` |
| QC | `quality-review-accounting` |
| Finalise | `finalisation-accounting` |
| Tax | `tax-accounting` |
| Contributor tooling | `accounting-builder-hub` |

## Layout

```
claude-for-accounting/
  .claude-plugin/marketplace.json
  shared/                 # guardrails, design framework, jurisdiction guide
  references/
    jurisdictions/        # country packs (malaysia first)
    notes-templates/      # disclosure scaffolds
    coa_templates/        # entity + industry
  scripts/                # validate + workbook/PDF generators
  managed-agent-cookbooks/
  <plugin>/skills/<skill>/SKILL.md
```

## Runtime config (not in git)

```
~/.claude/plugins/config/claude-for-accounting/
  firm-profile.md
  <plugin>/CLAUDE.md
  clients/<slug>/          # optional
```

## Design principles

1. **Pipeline fidelity** — stages match real engagement flow.  
2. **Traceability** — every number has a source.  
3. **White-label** — firm identity from cold-start only.  
4. **Jurisdiction as data** — packs under `references/jurisdictions/`.  
5. **SKILL.md carries doctrine** — CLAUDE.md is the safety net.  
6. **Validate in CI** — structural invariants before merge.

## Default firm seed

There is **no** default firm. Cold-start writes placeholders until the user answers.
