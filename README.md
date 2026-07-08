# Cynco Accounting Skills

Reference **agents, skills, and workflows** for Malaysian accounting engagements — from source documents to final signed financial statements, MPERS technical review, quality control, and tax computation.

Modelled on the architecture of [claude-for-legal](https://github.com/anthropics/claude-for-legal): **plugins by practice stage**, each with invocable skills, a firm practice profile written by a cold-start interview, and shared standards references.

> **Every output is a draft for accountant review.** These plugins accelerate compilation and year-end work. They do not replace a licensed professional, signed director approval, or auditor judgment.

## Engagement pipeline

```
Source Documents
      ↓
Bookkeeping (sales / purchases / receipts / payments / journals)
      ↓
Bank & Ledger Reconciliations
      ↓
Preliminary Trial Balance
      ↓
Year-End Adjustments
      ↓
Adjusted Trial Balance
      ↓
MPERS Technical Review
      ↓
Financial Statements + Notes
      ↓
Quality Review
      ↓
Final Signed Financial Statements
      ↓
Tax Computation & Statutory Filings
```

## Plugins

| Plugin | What it does |
|---|---|
| **engagement-accounting** | Firm cold-start, engagement setup, source-doc collection, client workspace, full-pipeline orchestrator |
| **bookkeeping-accounting** | Record & classify transactions; COA; journals |
| **reconciliation-accounting** | Bank + subledgers (AR/AP/inventory/FA/loans/tax); preliminary TB |
| **year-end-accounting** | YE adjustments (depreciation, accruals, prepayments, ECL, tax provision…); ATB |
| **mpers-accounting** | MPERS/MFRS technical review + disclosure checklist |
| **financial-statements-accounting** | SOFP, SOCI, SOCE, SCF, notes, compilation report, Excel workbook |
| **quality-review-accounting** | QC blockers, cross-ties, note consistency |
| **finalisation-accounting** | Lock, management approval, auditor pack, statutory handoff |
| **tax-accounting** | Form B/C/P/PT/TF/TP computations, capital allowances |

## Agents (skill commands)

| Agent / skill | Plugin | Command |
|---|---|---|
| Firm cold-start interview | engagement | `/engagement-accounting:cold-start-interview` |
| Engagement setup | engagement | `/engagement-accounting:engagement-setup` |
| Collect source documents | engagement | `/engagement-accounting:source-documents` |
| Full engagement pipeline | engagement | `/engagement-accounting:full-engagement-pipeline` |
| Record transactions | bookkeeping | `/bookkeeping-accounting:record-transactions` |
| Classify transactions | bookkeeping | `/bookkeeping-accounting:classify-transactions` |
| Bank reconciliation | reconciliation | `/reconciliation-accounting:bank-reconciliation` |
| Subledger reconciliations | reconciliation | `/reconciliation-accounting:subledger-reconciliations` |
| Preliminary TB | reconciliation | `/reconciliation-accounting:preliminary-trial-balance` |
| Year-end adjustments | year-end | `/year-end-accounting:year-end-adjustments` |
| Adjusted TB | year-end | `/year-end-accounting:adjusted-trial-balance` |
| MPERS technical review | mpers | `/mpers-accounting:mpers-technical-review` |
| Disclosure checklist | mpers | `/mpers-accounting:disclosure-checklist` |
| Primary statements | FS | `/financial-statements-accounting:prepare-primary-statements` |
| Notes to FS | FS | `/financial-statements-accounting:prepare-notes` |
| Quality review | QC | `/quality-review-accounting:quality-review` |
| Finalise accounts | finalisation | `/finalisation-accounting:finalise-accounts` |
| Tax computation | tax | `/tax-accounting:tax-computation` |

See each plugin’s `README.md` for the full skill list.

## Repository layout

```
engagement-accounting/           # setup + orchestrator
bookkeeping-accounting/
reconciliation-accounting/
year-end-accounting/
mpers-accounting/
financial-statements-accounting/
quality-review-accounting/
finalisation-accounting/
tax-accounting/
references/                      # MPERS, MFRS, tax, QC, entity types, COA
scripts/                         # generate_workbook.py, generate_pdf_report.py
shared/guardrails.md
.claude-plugin/marketplace.json
```

Each plugin:

```
<plugin>/
  .claude-plugin/plugin.json
  CLAUDE.md          # practice profile TEMPLATE (runtime config written elsewhere)
  README.md
  skills/<skill>/SKILL.md
  references/        # optional deep refs
```

## Getting started

See **[QUICKSTART.md](./QUICKSTART.md)**.

1. Add marketplace → install plugins  
2. `/engagement-accounting:cold-start-interview`  
3. `/engagement-accounting:engagement-setup`  
4. Run stage skills or `/engagement-accounting:full-engagement-pipeline`

## Framework selection (Malaysia)

| Entity | Framework (typical) | Tax form |
|---|---|---|
| Berhad (public) | MFRS | Form C |
| Sdn Bhd | MPERS | Form C |
| PLT | MPERS | Form PT |
| Sole prop | Accrual per S21A ITA | Form B |
| Partnership | Accrual per S21A ITA | Form P + B/BE |
| Koperasi | MCA standards | Form TF |
| Trust | MFRS/MPERS (varies) | Form TP |

## Core principles

1. Every number traces to a source document.  
2. Check documents before asking questions.  
3. MPERS / MFRS / ITA 1967 — no material shortcuts.  
4. Zero tolerance for imbalance (TB, BS, bank).  
5. Document decisions in working papers.

## Relationship to the legacy skill

The monolithic `accounting-workflow` skill (`~/.claude/skills/accounting-skills/`) is the predecessor. This marketplace **splits that workflow into stage plugins** so each phase can be invoked, reviewed, and improved independently — the same idea as legal practice-area plugins.

## License

See [LICENSE](./LICENSE). Accounting standards text is summarized for workflow use; authoritative standards remain MASB / MIA / LHDN publications.
