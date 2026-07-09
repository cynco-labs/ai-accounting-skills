---
name: capitalise-or-expense
description: Capitalise vs expense analysis for material money out (PPE, repairs, software). Use when capitalise or expense, fixed asset, renovation, repairs vs capex.
disable-model-invocation: true
---
# /capitalise-or-expense

## Purpose

Thin alias into **classify** — capital vs expense theme only.  
Doctrine: `shared/classify-substance.md`.  
Output: `workpapers/analysis/capital_vs_expense.md` (+ PPE notes if capitalised).

## Steps

1. Ensure `workpapers/transactions.json` exists (run **extract** if not).  
2. Set `classify_depth` = `standards_aware` for this theme.  
3. Load `references/jurisdictions/malaysia/standards/capital_vs_expense.md`.  
4. Follow **classify-transactions** steps 1–3 focused on material one-off / asset-like outflows.  
5. Write `workpapers/analysis/capital_vs_expense.md` from the analysis pack example.  
6. If capitalise: note FAR / depreciation policy needs (ask — do not invent rates).  
7. Apply COA codes; update payee_map; re-run classify for affected lines.

**Done when:** pack on disk with capitalise/expense/query per material outflow; codes applied or queried.

## Do not

- Invent useful lives or residual values  
- Capitalise owner personal spend  
- Expense all equipment into misc to avoid FAR without documenting the choice  
