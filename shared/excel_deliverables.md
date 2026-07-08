# Excel deliverables (openpyxl)

## What agents must know

| Fact | Implication |
|---|---|
| Workbooks are written with **openpyxl** (Python) | No Microsoft Excel app required to *generate* files |
| openpyxl does **not** run in a special sandbox | Same permissions as the agent shell / Python process |
| Formulas are stored as **strings** | Values appear after the user opens Excel or LibreOffice recalcs |
| Excel is **working papers**, not ledger SoR | After finalisation, push **Beancount** (`ledger/main.beancount`) |
| Money truth is proven in **Python/JSON** first | Never “fix” balances only inside Excel cells by hand |

## Scripts

| Script | Role |
|---|---|
| `scripts/generate_workbook.py` | Full engagement working papers (openpyxl) |
| `scripts/generate_pdf_report.py` | Reads xlsx via openpyxl → PDF |
| `scripts/extract_maybank_islamic_pdf.py` | Bank extract → formatted xlsx (+ optional JSON) |
| `scripts/export_to_beancount.py` | Journals → Beancount SoR (not Excel) |

## Dependencies

```bash
pip install -r requirements.txt
# minimum for Excel: pip install openpyxl
```

## Agent rules

1. Prefer **running repo scripts** over freestyle openpyxl in chat when a script exists.  
2. Prefer **JSON artifacts** (`transactions.json`, `journals.json`, `tb_*.json`) as machine truth.  
3. Excel is for **humans** (review, client packs).  
4. Do not claim formula results are calculated unless recalculated (Excel/LibreOffice).  
5. Client data paths stay local; no upload of xlsx to public paste sites.
