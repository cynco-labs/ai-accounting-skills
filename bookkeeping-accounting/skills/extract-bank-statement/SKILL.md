---
name: extract-bank-statement
description: >
  Extract bank PDF/CSV to transactions.json with running-balance proof
  (kernel: extract). Prefer CSV; Maybank Islamic PDF adapter when needed.
---
# /extract-bank-statement

## Purpose

Bank lines → structured transactions with **proof**, not vibes.

```text
pdfplumber / CSV  →  layout adapter  →  Decimal balance proof  →  Excel / JSON
```

## Preconditions

1. Read `shared/guardrails.md` and `references/bank_statement_extraction.md`.
2. Prefer **CSV/Excel export** from the bank portal when the user can provide it.
3. **Never invent lines.** Fail loud on balance breaks.

## Step 1 — Unified extract (required)

```bash
python3 scripts/extract_bank.py \
  --input /path/to/statements \
  --output ./outputs/bank.xlsx \
  --also-json ./workpapers/transactions.json \
  --client-slug <slug> \
  --fail-on-error

# detect only
python3 scripts/extract_bank.py --input /path/to/statements --detect-only

# CLI
npx @cynco/accounting-skills extract ./statements --out ./bank.xlsx --json ./txns.json
```

| Adapter | Status |
|---|---|
| `maybank_islamic_pdf` | Production (pdfplumber + line proof) |
| `cimb_csv` | Production (debit/credit CSV + balance proof) |
| `generic_csv` | Production (flexible headers) |
| Other PDF brands | Ask CSV — do not freestyle 1000 lines in chat |

Maybank-only direct script (still valid):

```bash
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank.xlsx \
  --also-json ./workpapers/transactions.json \
  --fail-on-error
```

## Step 2 — Verify

- `line_balance_ok` / open–close proof in extract meta  
- Spot-check first/last page against PDF  
- Write source register entry  

## Decision table

| Input | Action |
|---|---|
| Maybank Islamic PDF | `extract_bank` / Maybank script |
| CIMB / generic CSV | `extract_bank` CSV adapters |
| Other bank digital PDF | Prefer CSV; else new adapter (copy Maybank pattern) |
| Scanned image PDF | Ask for CSV or OCR pipeline — not vision freestyle |


## Completion

**Done when:** `transactions.json` (and optional xlsx) written, line/open–close balance proof passes (or **blocker** recorded), source register updated.

## Gates

- `--fail-on-error` must be set for production extracts  
- Zero fabricated transactions  
