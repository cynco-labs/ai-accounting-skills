---
name: extract-bank-statement
description: >
  Extract bank statements from PDF or CSV into a clean spreadsheet and/or
  transactions.json with running-balance proof. Use Maybank Islamic PDF adapter
  script for Maybank e-statements (pdfplumber + regex + Decimal proof — not
  vision). Trigger on bank PDF, bank CSV, Maybank statement, CIMB statement,
  "extract bank", "parse bank statement", convert statement to Excel, folder of
  monthly statements. Prefer CSV when available. Never invent lines. Fail loud
  on balance breaks.
---

# /extract-bank-statement

## Purpose

Turn bank PDFs/CSVs into **accurate, machine-checkable** transaction registers **quickly**.

This skill encodes the **proven method** (used on real Maybank Islamic multi-month books):

```text
pdfplumber text  →  layout adapter  →  Decimal balance proof  →  Excel / JSON
```

**Not:** vision-first bulk reading of digital e-statements.

Load: `references/bank_statement_extraction.md`

## Preconditions

1. `shared/guardrails.md` — no fabricated numbers  
2. Input path: file or folder the user gave  
3. Dependencies: `pdfplumber`, `openpyxl` (`pip install pdfplumber openpyxl`)  
4. Optional schema: `references/schemas/transactions.schema.json`

## Step 0 — Detect input type (do this first)

| Signal | Path |
|---|---|
| `.csv` / `.xlsx` export | `scripts/normalize_bank_csv.py` |
| PDF text contains `Maybank Islamic` / `結單日期` / `戶號` / `SME FIRST INVESTMENT` | **`scripts/extract_maybank_islamic_pdf.py`** |
| PDF has little/no extractable text | OCR/vision **last resort**; ask for CSV if possible |
| Other bank digital PDF | Prefer CSV; else new adapter (do not freestyle 1000 lines in chat) |

Quick probe:

```bash
python3 -c "import pdfplumber; p=pdfplumber.open('FILE.pdf'); print((p.pages[0].extract_text() or '')[:800])"
```

## Step 1 — Prefer bank CSV (tell the user once if PDF is painful)

If PDF is scanned or unknown layout:

> “If you can export CSV/Excel from Maybank2u, extraction will be faster and safer. Meanwhile I’ll try the PDF adapter.”

## Step 2 — Run the adapter (Maybank Islamic)

From the **repo root** of claude-for-accounting (or any checkout that has `scripts/`):

```bash
python3 scripts/extract_maybank_islamic_pdf.py \
  --input "/path/to/folder-or.pdf" \
  --output "/path/to/Client_Bank_Transactions.xlsx" \
  --also-json "/path/to/workpapers/transactions.json" \
  --client-slug "client-slug" \
  --fail-on-error
```

### What the script does (agents must not re-invent unless adapting a new bank)

1. Open each PDF with **pdfplumber**  
2. Read **text lines** (ignore unusable mega-tables)  
3. Parse `DD/MM TYPE amount± balance`  
4. Attach continuation lines as counterparty detail (strip footers)  
5. Prove every line: `prior_balance ± amount == statement_balance`  
6. Prove month: `begin + inflows − outflows == end`  
7. Write Excel: Summary, All Transactions, per-period sheets, QA_Checks  
8. Optional `transactions.json` for the engagement pipeline  

### Pass / fail (report to user)

| Check | Required |
|---|---|
| Line balance | PASS every file |
| Open → close | PASS every file |
| Cross-month continuity | PASS when consecutive months present |
| Footer TOTAL DEBIT/CREDIT vs sums | Informational (Maybank footers can differ; line chain is source of truth) |

If `--fail-on-error` and any FAIL → **stop**. Show the break. Do not hand-edit amounts to “make it work.”

## Step 3 — CSV path

```bash
python3 scripts/normalize_bank_csv.py \
  --input export.csv \
  --bank-id maybank-001 \
  --source-file source/bank/export.csv \
  --client-slug client-slug \
  --output workpapers/transactions_partial.json
```

Then map into Excel or merge into the client register.

## Step 4 — Engagement artifacts

If inside an engagement workspace:

- Save xlsx under `outputs/` or client root  
- Save JSON as `workpapers/transactions.json`  
- Update `source/register.md`  
- Update `engagement_state.json` (`record_transactions` progress)  
- Next: `classify-transactions` (do not classify inside extract unless user asks)

## Step 5 — Scanned PDF / vision (only if no text)

1. Tell user accuracy risk is higher  
2. Prefer: request CSV  
3. If proceeding: process **page by page**, store `source_ref=page:N`, mark `confidence=low` rows  
4. Still run recon to statement closing balance when known  
5. Never invent a line to fix recon  

## Efficiency rules (why this is “fast”)

1. **Batch code**, not per-line LLM reading  
2. **Same layout → same adapter** (new months are free)  
3. **Balance proof is O(n)** and catches errors machines make  
4. Re-run whole folder is fine for &lt;20 monthly PDFs; optional future: skip already-hashed files  

Agents **must run the script** for Maybank Islamic rather than re-deriving the regex in chat when the script is available.

## Failure modes

| Failure | Action |
|---|---|
| No text in PDF | Ask CSV; optional vision with warnings |
| Balance break | Print row context; fix parser or source; do not fudge |
| Missing month in folder | Note gap; do not interpolate |
| Unknown bank layout | Do not force Maybank parser; ask CSV or add adapter |

## Outputs checklist

- [ ] `.xlsx` with Summary + All Transactions + periods + QA  
- [ ] PASS/FAIL printed per file  
- [ ] Optional `transactions.json`  
- [ ] Source provenance (file + page) on every row  

## Next skill

`classify-transactions` → `journal-entries` → `bank-reconciliation`
