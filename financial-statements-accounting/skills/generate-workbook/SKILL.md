---
name: generate-workbook
description: >
  Build Excel workpapers pack via openpyxl. Use when working papers Excel
  or workbook.
---
# /generate-workbook

## Purpose

Single-pass **Excel working papers** for human review and client packs.

Uses **openpyxl** (Python). Does not require Microsoft Excel to generate. 
Formulas are written as strings — values appear when the file is opened/recalculated.

See `shared/excel_deliverables.md`. 
Ledger SoR after finalisation: **Beancount** (`export-beancount`), not this xlsx.

## Script

```bash
pip install openpyxl # or: pip install -r requirements.txt
python3 scripts/generate_workbook.py <input.json> <output.xlsx>
```

## Expected sheets (minimum)

1. Company Info 
2. Chart of Accounts 
3. Bank Transactions 
4. Payroll Summary 
5. Fixed Asset Register 
6. Journal Entries 
7. General Ledger 
8. Trial Balance 
9. Income Statement 
10. Balance Sheet 
11. Tax Computation 
12. Queries & Notes 

## Process

1. Assemble classified data + ATB + YE JEs into the script’s input JSON format. 
2. Run the generator. 
3. Verify file opens; spot-check TB/BS. 
4. Machine truth remains in `workpapers/*.json` — do not invent numbers in Excel only. 

## PDF

Optional: `scripts/generate_pdf_report.py` (reads xlsx via openpyxl, needs `reportlab`).

## Completion

**Done when:** workbook opens without corruption and key sheets tie to JSON workpapers/TB.

