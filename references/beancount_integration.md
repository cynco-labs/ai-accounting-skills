# Beancount + Fava — native ledger integration

## Architecture (what agents must know)

```text
Source PDFs/CSV
    → extract / classify / journals (JSON)
    → Excel workpapers (openpyxl)     ← human review pack, NOT system of record
    → QC + finalise
    → Beancount (.beancount)         ← SYSTEM OF RECORD for the ledger
    → Fava (web UI)                  ← impress / explore / share locally
```

| Layer | Role | Tool |
|---|---|---|
| **Working papers** | Engagement drafts, classification, YE, FS drafts | JSON + openpyxl Excel |
| **System of record** | Final double-entry ledger, git-friendly, auditable text | **Beancount** |
| **Presentation UI** | Browse balances, journals, P&L/BS interactively | **Fava** |

Coding agents often only “know Excel.”  
**Beancount is the final boss:** after numbers are solid, push the ledger here.

## When to export

| Moment | Action |
|---|---|
| After journals balance + TB balances | Optional draft ledger (`ledger/draft.beancount`) |
| After QC Section A PASS + finalise | **Required for full engagements:** `ledger/main.beancount` |
| User says “open Fava” / “show me the books” | `open-fava` on the ledger |

Do **not** push garbage or unbalanced journals. Export fails by default if a JE does not balance.

## Commands

```bash
# From engagement client folder
python3 scripts/export_to_beancount.py \
  --client-dir clients/acme-sdn-bhd \
  --output clients/acme-sdn-bhd/ledger/main.beancount \
  --bean-check

# Explicit inputs
python3 scripts/export_to_beancount.py \
  --journals workpapers/journals.json \
  --journals-ye workpapers/journals_ye.json \
  --coa references/coa_templates/coa_sdn_bhd.json \
  --currency MYR \
  --title "ACME SDN. BHD." \
  --output ledger/main.beancount \
  --bean-check

# UI
scripts/run_fava.sh clients/acme-sdn-bhd/ledger/main.beancount
# → http://127.0.0.1:5000
```

## Install (user machine)

```bash
pip install beancount fava
# optional
bean-check ledger/main.beancount
fava ledger/main.beancount
```

## Account mapping

COA codes map to Beancount hierarchies:

| COA type | Beancount root |
|---|---|
| Asset | `Assets:…` |
| Liability | `Liabilities:…` |
| Equity | `Equity:…` |
| Revenue | `Income:…` |
| Expense | `Expenses:…` |

Example: `1000 Cash & Bank` → `Assets:Cash-And-Bank-1000`

Sidecar: `main.beancount.account_map.json` (code → Beancount name).

## Engagement artifacts

| Path | Meaning |
|---|---|
| `ledger/main.beancount` | Final / primary ledger SoR |
| `ledger/draft.beancount` | Optional pre-final export |
| `ledger/main.beancount.account_map.json` | Code mapping |
| `outputs/workpapers.xlsx` | Human working papers (still useful) |

## Skills

| Skill | Does |
|---|---|
| `export-beancount` | Build ledger from journals + COA |
| `validate-beancount` | `bean-check` + continuity notes |
| `open-fava` | Launch Fava on the ledger |

## Agent rules

1. Excel is **not** the ledger SoR after finalisation — Beancount is.  
2. Always run `bean-check` (or skill validate) before telling the user Fava is ready.  
3. Fava is local-only by default (`127.0.0.1`) — do not expose publicly without user consent.  
4. If Beancount/Fava not installed, give `pip install` once; do not fake a UI.  
5. Re-export after any post-lock journal change; keep ledger in git if client allows.

## Pipeline position

```text
… → quality_review → finalisation → export-beancount → open-fava (optional)
                              ↘ tax (from same locked figures)
```
