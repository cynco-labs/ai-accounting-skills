---
name: classify-transactions
description: >
  Categorize transactions to the chart of accounts (prior-year map, patterns,
  invoices, then staff Q&A). Trigger on "classify", "code these", "what account",
  uncategorized transactions, suspense clean-up, payee mapping.
---
# /classify-transactions

## Purpose

Assign account codes correctly. **Accuracy over speed.** Deterministic first pass, then agent adjudication.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Resolve firm profile (`shared/firm-profile.md` / `python3 scripts/resolve_firm_profile.py`).
3. Load active client engagement workspace.
4. **Never fabricate numbers.** Re-read source documents if figures are missing from context.

## Step 0 — Run the classifier (required)

```bash
python3 scripts/classify_transactions.py \
  --input workpapers/transactions.json \
  --output workpapers/transactions.json \
  --payee-map workpapers/payee_map.json \
  --report workpapers/classification_review.md

# or
npx @cynco/accounting-skills classify ./workpapers/transactions.json
```

Rules live in `references/classification_patterns.json` (Malaysia defaults).  
Payee map (optional): `workpapers/payee_map.json` — `{ "acme sdn bhd": { "account_code": "4000", "account_name": "Revenue" } }`.

| Field | Meaning |
|---|---|
| `classification_basis` | `prior_year` · `pattern` · `invoice` · `employee` · `suspense` |
| `classification_confidence` | 0–1 |
| `needs_review` | Agent must confirm |

**Do not re-derive pattern tables in chat** when the script exists.

## Priority order (after script)

### 1. Review queue only
Open `classification_review.md`. For each `needs_review` row:

- Confirm pattern suggestion, or  
- Ask staff with 3–5 account options, or  
- Suspense + query sheet (last resort)

### 2. Invoice matching
Match amount ± date window to purchase/sales invoices → basis `invoice`.

### 3. Industry overlay
If engagement has an industry overlay, apply `classification_hints` from `references/coa_templates/industry/*.json`.

### 4. Update payee map
Write confirmed payees back to `workpapers/payee_map.json` for next year.

## Output

`workpapers/transactions.json` with `account_code`, `account_name`, `classification_basis`, `classification_confidence`, `needs_review`.

## Gates

- No silent suspense for material payroll / tax / related-party lines — escalate.  
- Never invent amounts.  
