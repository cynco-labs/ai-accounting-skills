---
name: journal-entries
description: >
  Post classified transactions to balancing double-entry journals via
  scripts/post_journals.py (kernel: post). Trigger on journals, postings,
  double entry, JE list, "post the books". Then roll TB with roll_tb.py —
  do not freestyle trial balances.
---
# /journal-entries

## Purpose

Convert classified activity into double-entry journals. **Engine posts; agent judges openings/exceptions.**

Load `shared/kernel-contract.md` and `shared/guardrails.md`.

## Step 1 — Post (required)

```bash
python3 scripts/post_journals.py \
  --client-dir <client> \
  --bank-code 1000 \
  --opening-from-bank

# or with explicit openings pack
python3 scripts/post_journals.py \
  --transactions workpapers/transactions.json \
  --output workpapers/journals.json \
  --openings workpapers/journals_opening.json \
  --bank-code 1000

npx @cynco/accounting-skills post <client> --opening-from-bank
```

| Input | Rule |
|---|---|
| Classified `transactions.json` | Every line has `account_code` (or fail) |
| Inflow | DR bank · CR code |
| Outflow | DR code · CR bank |
| Openings | `--openings` file or `--opening-from-bank` (equity offset) |

**Do not** re-derive bank JEs line-by-line in chat when the script exists.

## Step 2 — Roll preliminary TB (required)

```bash
python3 scripts/roll_tb.py --client-dir <client> --preliminary
npx @cynco/accounting-skills tb <client> --preliminary
```

TB totals are **never** typed by the agent.

## Manual / non-bank journals

Client-supplied or payroll/sales books: append balancing JEs to `journals.json` (same schema), then re-run `roll_tb`. Each JE must balance or the roll fails.

## Gates

- Every JE: Σ DR = Σ CR  
- No blank accounts  
- Prelim TB difference = 0  

## Output

`workpapers/journals.json` + `workpapers/tb_preliminary.json`.  
Next: bank recon → YE adjustments → `roll_tb --adjusted`.
