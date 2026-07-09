# Stage artifact contracts

A stage is complete only when **required artifacts** exist and **gates** pass.
Paths are relative to `clients/<slug>/`.

| Stage | Required artifacts | Gate |
|---|---|---|
| setup | `README.md`, `engagement_state.json` | Entity, FY, framework known; **`operator`** + **`engagement_type`** set (`shared/operator-lens.md`); shelf layout exists |
| source_documents | `source/register.md` (+ files under `source/**` or `_pointers.md`) | Bank coverage green/amber (red = blocked unless override logged); shelf-first done |
| record_transactions | `workpapers/transactions.json` (or `.csv`) | Every bank line extracted for in-scope periods |
| classify_transactions | `workpapers/transactions.json` with `account_code` on each row; if `classify_depth=standards_aware`, material themes under `workpapers/analysis/` | No silent suspense; unresolved → queries; standards-aware: analysis packs or with-limitation |
| journal_entries | `workpapers/journals.json` | Every JE balances |
| bank_reconciliation | `workpapers/reconciliations/bank_*.md` | Diff = 0.00 |
| subledger_reconciliations | `workpapers/reconciliations/subledgers.md` | Material controls tied or queried |
| preliminary_trial_balance | `workpapers/tb_preliminary.json` | DR = CR — **only via `scripts/roll_tb.py`** |
| year_end_adjustments | `workpapers/journals_ye.json` | Catalogue considered; AJEs posted & balanced |
| adjusted_trial_balance | `workpapers/tb_adjusted.json` | DR = CR via **`roll_tb.py`**; **source of truth for FS** |
| standards_review | `workpapers/standards_review.md` | Issues → AJE or disclosure list |
| primary_statements | `outputs/fs/primary_statements.md` (or xlsx sheet) | BS balances; mapping from ATB |
| notes | `outputs/fs/notes.md` | Notes tie to primaries |
| quality_review | `workpapers/qc_report.md` | Section A all pass |
| finalisation | `outputs/fs/FINAL_STATUS.md` | Locked + approval recorded (or pending_approval) |
| beancount_sor | `ledger/main.beancount` | `bean-check` PASS — **ledger system of record** |
| tax | `outputs/tax/computation.md` | Ties to locked P&L if final |

**Human pack (all depths that claim Done):** `outputs/<slug>_pack.html` via `scripts/generate_html_report.py` — required by `depth_gates` (`check: html_pack`). Fresh vs TB. This is the user handoff; not Fava.

## Optional but recommended

| Artifact | When |
|---|---|
| `workpapers/coa.json` | After COA selected |
| `workpapers/far.json` | PPE present |
| `workpapers/payee_map.json` | Returning clients / for next year |
| `workpapers/analysis/*.md` | Standards-aware classify (revenue, capital vs expense, …) |
| `workpapers/queries.md` | Paper trail of asks only — not the user UI |
| `outputs/workpapers.xlsx` | After generate-workbook (staff; not SoR) |
| `ledger/draft.beancount` | Mid-engagement preview |
| `ledger/main.beancount.account_map.json` | COA code → Beancount account map |

## Agent checks

Before claiming progress:

```text
1. Does engagement_state.json exist?
2. Does current_stage match the work about to run?
3. Do required artifacts for prior stages exist?
4. Are blockers empty or explicitly waived?
```
