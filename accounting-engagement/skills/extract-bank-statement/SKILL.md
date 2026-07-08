---
name: extract-bank-statement
description: >
  Extract bank statement lines from PDF or CSV into the transactions register
  schema (workpapers/transactions.json). Trigger on bank PDF, bank CSV, Maybank
  statement, CIMB statement, "extract bank", "parse bank statement", import
  bank export, convert statement to transactions. Runs before classify. Never
  invents lines for missing months.
---

# /extract-bank-statement

## Purpose

Turn **bank PDFs/CSVs** into machine-checkable `workpapers/transactions.json` rows with source provenance. This is the weak link most agents freestyle — do it explicitly.

## Preconditions

1. `shared/guardrails.md`
2. Active client workspace (or create via engagement-setup)
3. Schema: `references/schemas/transactions.schema.json`
4. Optional helper: `scripts/normalize_bank_csv.py`

## Inputs

| Format | Handling |
|---|---|
| **CSV / Excel export** | Prefer `normalize_bank_csv.py` or map columns manually |
| **PDF e-statement** | Extract text/tables; every line needs date, description, amount, direction |
| **Scanned image PDF** | OCR if available; flag low-confidence rows for human review |

## Workflow

### 1. Identify account & period

- Bank name, account last4 if present
- Statement period start/end
- Opening and closing balances from statement

### 2. Extract every movement line

For each line produce:

```json
{
  "id": "txn-YYYYMMDD-###",
  "date": "YYYY-MM-DD",
  "description": "...",
  "amount": 123.45,
  "direction": "inflow|outflow",
  "bank_account_id": "...",
  "running_balance": 0,
  "account_code": null,
  "classification_basis": null,
  "source_file": "source/bank/....",
  "source_ref": "page:3|row:12"
}
```

**Do not classify here** unless the user asked for a combined pass — leave `account_code` null for `classify-transactions`.

### 3. Continuity checks (blockers)

- Opening balance = prior statement closing (or zero / documented)
- Each running balance follows prior ± movement (if statement provides running bal)
- Closing balance = last statement balance
- No month gaps for the engagement period

### 4. Write artifacts

- Append/merge into `workpapers/transactions.json` (schema 0.0.1)
- Update `source/register.md`
- Update `engagement_state.json`: stage `record_transactions` in progress or complete when full period extracted
- Run: `python3 scripts/validate_engagement_artifacts.py <client_dir>`

### 5. CSV helper

```bash
python3 scripts/normalize_bank_csv.py \
  --input path/to/export.csv \
  --bank-id maybank-001 \
  --source-file source/bank/export.csv \
  --output workpapers/transactions_partial.json
```

Merge partial into the client register carefully (no duplicate ids).

## Direction convention

| Statement shows | direction |
|---|---|
| Credit / deposit / money in | `inflow` |
| Debit / withdrawal / money out | `outflow` |
| amount always **positive** | yes |

## Failure modes

| Failure | Behavior |
|---|---|
| Unreadable PDF | Ask for CSV export; do not guess lines |
| Missing month | Blocker or AMBER limitation in state |
| Balance doesn't roll | Stop; list break point |
| FX multi-currency | Separate bank_account_id per currency; note rate source |

## Next skill

`record-transactions` (if more non-bank books) → `classify-transactions`
