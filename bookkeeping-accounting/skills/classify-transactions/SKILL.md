---
name: classify-transactions
description: >
  Classify bank lines to the chart of accounts — with substance under MPERS/MFRS
  when standards-aware. Use when classify, code these, do the classifications,
  uncategorized transactions, revenue recognition, capitalise or expense, payee mapping.
---
# /classify-transactions

## Purpose

**Codes are the end of classify. Substance is the middle.**

Main job: **classify**.  
Doctrine: `shared/classify-substance.md`.  
Script first for baseline; agent applies economic substance for material themes when depth requires it.

## Preconditions

1. `shared/guardrails.md` + firm profile if present.  
2. Active engagement; `workpapers/transactions.json` exists (**extract** done).  
3. Framework known or provisional (`engagement_state.json`).  
4. Re-read sources if context was compacted (**files are the books**).  
5. Load `shared/classify-substance.md` and choose **`classify_depth`**:  
   - `bookkeeping` — fast path  
   - `standards_aware` — year-end / “proper classifications” / revenue or capex questions  

Write `classify_depth` into state (`notes` or `artifacts` map) when set.

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
Payee map (optional): `workpapers/payee_map.json`.

| Field | Meaning |
|---|---|
| `classification_basis` | `prior_year` · `pattern` · `invoice` · `employee` · `suspense` · `analysis` |
| `classification_confidence` | 0–1 |
| `needs_review` | Agent must confirm |

Do not re-derive pattern tables in chat when the script exists.

**Done when:** script exit 0 and `classification_review.md` written.

### 2 — Money map (material themes)

From `transactions.json` + review report, group **material** lines:

| Theme | Signal | Checklist (Malaysia pack) | Analysis file |
|---|---|---|---|
| Revenue | Material credits / customer-like inflows | `references/jurisdictions/malaysia/standards/revenue_recognition.md` | `workpapers/analysis/revenue_recognition.md` |
| Capital vs expense | Material one-off / asset-like outflows | `…/standards/capital_vs_expense.md` | `workpapers/analysis/capital_vs_expense.md` |
| Related parties | Directors / shareholders / common control | `references/mpers.md` S33 | `workpapers/analysis/related_parties.md` |

Materiality guide: ~RM500 cluster, or any statutory/related-party, or firm materiality.

**Bookkeeping depth:** skip to step 4 (review queue only) unless a line is statutory/related-party.

**Standards-aware depth:** continue step 3 for every material theme.

**Done when:** theme list written (can live at top of `classification_review.md` or `workpapers/analysis/README.md`).

### 3 — Substance analysis (standards-aware)

For each material theme:

1. Load the country checklist (not model memory for the standard).  
2. Walk decision points against **sources** (bank pages, invoices).  
3. **Structured ask** ≤3 questions per theme if judgment is open (`shared/user-questions.md`).  
4. Write the analysis pack using `references/schemas/analysis_pack.example.md`.  
5. Record conclusion → COA codes; set `classification_basis` to `analysis` where codes come from the pack.

**Done when:** every material theme has a pack with conclusion **or** open query logged; no silent “all sales / all misc.”

### 4 — Adjudicate remaining review queue

Open `classification_review.md`. For material `needs_review` rows not already settled by analysis:

- Confirm pattern suggestion, or  
- Structured ask with 3–5 account options, or  
- Suspense + query (last resort)

Mandatory for material batches: host question tool when available.

After answers: update `payee_map.json`, re-run classify script.

Optional: invoice match; industry `classification_hints` from `references/coa_templates/industry/*.json`.

**Done when:** every material `needs_review` row confirmed, queried, or suspense+query.

### 5 — Hand off to post

**Done when:**

- `transactions.json` has coherent codes / names / basis / confidence  
- **If standards_aware:** required analysis packs exist for material revenue and capital-vs-expense themes (or explicit **with limitation** in state)  
- `payee_map.json` updated for confirmed recurring payees  

Next: **post** (`journal-entries` → `post_journals.py`).

## Gates

- No silent suspense for material payroll / tax / related-party.  
- Never invent amounts.  
- Never invent useful lives, residual values, or recognition policy — ask or use prior-year/firm policy.  
- Standards-aware: material money-in coded as revenue without `revenue_recognition.md` → incomplete (must stop or with limitation).

## Failure modes

| Failure | Behavior |
|---|---|
| Ambiguous payee | Structured ask; then suspense if still open |
| Agent codes without script | Re-run classifier; discard bulk freestyle codes |
| Agent skips substance on year-end job | Force standards_aware path; write packs |
| Premature “all classified” | Exhaustive bar on material review + material themes |

## Output

| Path | Role |
|---|---|
| `workpapers/transactions.json` | Lines + codes |
| `workpapers/classification_review.md` | Review queue |
| `workpapers/payee_map.json` | Recurring map |
| `workpapers/analysis/*.md` | Substance conclusions (standards-aware) |

## Thin branches (same skill)

If user only asks one theme, still write that theme’s analysis pack and only force that theme’s codes — then stop or continue full classify as they prefer.

- Revenue only → load revenue checklist  
- Capitalise or expense only → load capital checklist  
