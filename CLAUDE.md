# Cynco Accounting Skills — Repo Guide

This repository is a **Claude Code / Cowork plugin marketplace** for Malaysian accounting engagements, structured like [claude-for-legal](https://github.com/anthropics/claude-for-legal): practice-area plugins, granular skills, firm practice profiles, and shared references.

## Design principles

1. **Pipeline fidelity** — skills map to real engagement flow (source docs → FS → QC → finalise → tax).
2. **Traceability** — every number has a source; no fabrication.
3. **Firm-specific** — cold-start interview writes a practice profile every skill reads.
4. **Progressive disclosure** — load only the reference files the current stage needs.
5. **Gates** — mathematical blockers stop the pipeline; overrides are explicit and logged.

## Plugin map → engagement pipeline

| Stage | Plugin | Key skills |
|---|---|---|
| Firm + engagement setup | `engagement-accounting` | cold-start-interview, engagement-setup, source-documents, client-workspace, full-engagement-pipeline |
| Record & classify | `bookkeeping-accounting` | record-transactions, classify-transactions, chart-of-accounts, journal-entries |
| Reconcile + TB | `reconciliation-accounting` | bank-reconciliation, subledger-reconciliations, preliminary-trial-balance |
| Year-end | `year-end-accounting` | year-end-adjustments, adjusted-trial-balance |
| Standards | `mpers-accounting` | mpers-technical-review, disclosure-checklist |
| Statements | `financial-statements-accounting` | prepare-primary-statements, prepare-notes, compilation-report, generate-workbook |
| QC | `quality-review-accounting` | quality-review, cross-tie-check |
| Finalise | `finalisation-accounting` | finalise-accounts, management-approval, auditor-pack, statutory-handoff |
| Tax | `tax-accounting` | tax-computation, capital-allowances |

## Layout

```
cynco-accounting-skills/
  .claude-plugin/marketplace.json
  shared/guardrails.md
  references/                 # shared MPERS, tax, COA, QC, etc.
  scripts/                    # workbook + PDF generators
  <plugin>/
    .claude-plugin/plugin.json
    CLAUDE.md                 # firm/engagement profile TEMPLATE
    README.md
    skills/<skill>/SKILL.md
    references/               # plugin-local deep refs
```

## Config (runtime, not in git)

```
~/.claude/plugins/config/cynco-accounting-skills/
  firm-profile.md
  engagement-accounting/CLAUDE.md
  <other-plugins>/CLAUDE.md   # if they write plugin-specific prefs
  clients/<client-slug>/      # engagement working papers (optional path)
```

## Non-negotiables for contributors

- Read `shared/guardrails.md` before editing skills.
- Skills that produce numbers must restate source provenance.
- Do not collapse the pipeline into one opaque skill without keeping stage skills invocable.
- Keep SKILL.md frontmatter `name` and `description` accurate for auto-invocation.

## Default firm (template seed)

```yaml
firm_name: "Hazli Johar & Co."
registration: "Chartered Accountants (NF1932)"
contact: "hazli@hazlijohar.my"
```

White-label by running cold-start-interview or editing the firm profile.
