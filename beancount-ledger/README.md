# beancount-ledger

**Beancount** = system of record for the double-entry ledger.  
**Fava** = beautiful local web UI on top of that ledger.

Excel/openpyxl workpapers stay for engagement review. When books are solid, agents push here.

## Skills

| Skill | Command idea |
|---|---|
| `export-beancount` | Journals + COA → `.beancount` |
| `validate-beancount` | `bean-check` |
| `open-fava` | Serve Fava on the ledger |

## Quick start

```bash
pip install beancount fava

python3 scripts/export_to_beancount.py \
  --client-dir path/to/client \
  --output path/to/client/ledger/main.beancount \
  --bean-check

scripts/run_fava.sh path/to/client/ledger/main.beancount
```

See `references/beancount_integration.md` (repo root).
