---
name: generate-workbook
description: >
  Generate Excel working-papers workbook via scripts/generate_workbook.py.
  Trigger on working papers excel, workpapers xlsx, generate workbook.
---
# /generate-workbook

## Purpose

Single-pass Excel workpapers.

## Script
Repo: `scripts/generate_workbook.py`  
(Legacy: also under `~/.claude/skills/accounting-skills/scripts/`)

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
1. Assemble classified data + ATB + YE JEs into the script's input format.
2. Run the generator.
3. Open and verify file is not corrupt; spot-check TB and BS formulas.

## PDF
Optional: `scripts/generate_pdf_report.py` for client-facing FS PDF (B&W).
