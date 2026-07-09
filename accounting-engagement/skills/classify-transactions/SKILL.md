---
name: classify-transactions
description: >
  Classify bank lines to COA codes (kernel: classify). Use when classify,
  code these, uncategorized transactions, suspense clean-up, or payee
  mapping.
---
# /classify-transactions

## Purpose

Assign account codes correctly. Intent: **classify**. Deterministic script first; agent adjudicates the review queue only.

## Preconditions

1. `shared/guardrails.md` + firm profile if present.
2. Active engagement; `workpapers/transactions.json` exists (from **extract**).
3. Re-read sources if figures missing from context (**disk is truth**).

## Steps

### 1 — Run the classifier (required)

```bash
python3 scripts/classify_transactions.py \
  --input workpapers/transactions.json \
  --output workpapers/transactions.json \
  --payee-map workpapers/payee_map.json \
  --report workpapers/classification_review.md

# or
npx @cynco/accounting-skills classify ./workpapers/transactions.json
```

Rules: `references/classification_patterns.json`.  
Payee map (optional): `workpapers/payee_map.json` —  
`{ "acme sdn bhd": { "account_code": "4000", "account_name": "Revenue" } }`.

| Field | Meaning |
|---|---|
| `classification_basis` | `prior_year` · `pattern` · `invoice` · `employee` · `suspense` |
| `classification_confidence` | 0–1 |
| `needs_review` | Agent must confirm |

Do not re-derive pattern tables in chat when the script exists (**kernel**).

**Done when:** script exit 0 and `classification_review.md` written.

### 2 — Adjudicate the review queue

Open `classification_review.md`. For **material** `needs_review` rows (batch by payee/pattern):

- Confirm pattern suggestion, or  
- **Structured ask** with 3–5 account options (`shared/user-questions.md`), or  
- Suspense + query sheet (last resort)

Mandatory for material batches (≥ ~RM500 or statutory/related-party): host question tool, ≤3 batched questions — not prose-only options.

After answers: update `workpapers/payee_map.json`, re-run classify.

Optional: invoice match (amount ± date → basis `invoice`); industry `classification_hints` from `references/coa_templates/industry/*.json`.

**Done when:** every material `needs_review` row is confirmed, queried, or suspense+query; payee_map updated for confirmed payees.

### 3 — Hand off to post

**Done when:** `transactions.json` has `account_code` / `account_name` / basis / confidence / `needs_review` coherent with the review file.

## Gates

- No silent suspense for material payroll / tax / related-party — escalate.  
- Never invent amounts.

## Failure modes

| Failure | Behavior |
|---|---|
| Ambiguous payee | Structured ask; then suspense if still open |
| Agent codes without script | Re-run classifier; discard freestyle bulk codes |
| Premature “all classified” | Exhaustive bar on material review rows |

## Output

`workpapers/transactions.json` + `classification_review.md` + updated `payee_map.json`.  
Next intent: **post** (`journal-entries` → `post_journals.py`).
