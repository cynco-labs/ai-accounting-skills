# Bank statement extraction — agent method (proven)

## Design principle

**Do not rely on vision for bulk bank books when a text layer exists.**

```text
Prefer:  Bank CSV/OFX export
Then:    Digital PDF + layout adapter + running-balance proof
Last:    Vision/OCR page-by-page with confidence flags + recon
Never:   Invent missing months or force TB balance
```

## Adapter ladder (what agents must do)

| Priority | Input | Tool | Proof |
|---|---|---|---|
| 1 | CSV / Excel / OFX | `scripts/normalize_bank_csv.py` | Column map + totals |
| 2 | Maybank Islamic e-statement PDF | `scripts/extract_maybank_islamic_pdf.py` | Line balance chain + open→close |
| 3 | Other digital PDF | New adapter (copy Maybank pattern) | Same proofs |
| 4 | Scanned image PDF | OCR/vision **per page** | Human review + recon; flag low confidence |

## Maybank Islamic method (productionized)

**Script:** `scripts/extract_maybank_islamic_pdf.py`  
**Skill:** `extract-bank-statement` (routes here when Maybank detected)

### Stack

- `pdfplumber` — extract text (not table blobs for this layout)
- Regex line parser — `DD/MM TYPE amount± balance`
- `Decimal` — money math
- `openpyxl` — Excel deliverable
- Optional JSON → `references/schemas/transactions.schema.json`

### Why not tables / vision for this bank

Maybank e-statements yield **one huge table cell** via `extract_tables()`.  
Real structure is **line-oriented text**. Vision is slower and can mis-read amounts.

### Agent commands

```bash
# Folder of monthly PDFs → Excel
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/CJT-BS-2026 \
  --output /path/to/CJT_transactions.xlsx \
  --also-json /path/to/workpapers/transactions.json \
  --client-slug cjt-bakery-sdn-bhd \
  --fail-on-error

# Single PDF
python3 scripts/extract_maybank_islamic_pdf.py \
  --input ./Jan26.pdf \
  --output ./Jan26.xlsx
```

### Pass criteria (must report)

1. **Line balance:** every row `prev ± amount = statement balance`  
2. **Open→close:** `begin + inflows − outflows = end`  
3. **Cross-month:** month N end = month N+1 begin (when consecutive months present)  
4. **No invented rows**  

If fail → stop, show break, re-extract or ask for CSV. Do not patch numbers.

### Output sheets

- Summary (per file QA)  
- All Transactions  
- One sheet per period (`YYYY-MM`)  
- QA_Checks  

## Adding another bank

1. Save 1 sample PDF under `fixtures/bank-samples/<bank>/` (synthetic or redacted)  
2. Copy `extract_maybank_islamic_pdf.py` → `extract_<bank>_pdf.py`  
3. Adjust header/date/amount regex only  
4. Keep the **same proof functions**  
5. Register in `extract-bank-statement` skill detection table  
6. Document in this file  

## Skill routing

| Signal in files / text | Action |
|---|---|
| `Maybank Islamic`, `結單日期`, `戶號`, `DUITNOW` | Maybank Islamic script |
| `.csv` bank export | `normalize_bank_csv.py` |
| Unknown PDF, no text | Vision/OCR path + warn; prefer client CSV |

## What agents must not do

- Re-implement a half parser in chat without running the script when the script applies  
- Accept extract without printing PASS/FAIL for balance checks  
- Merge months without checking continuity  
- Use vision first on digital Maybank PDFs  
