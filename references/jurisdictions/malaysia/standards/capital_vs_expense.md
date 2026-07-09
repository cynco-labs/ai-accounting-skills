# Malaysia — Capitalise vs expense checklist (workflow summary)

**Not official MASB text.** Verify against current MPERS / MFRS and firm policy.  
Use when classifying **material money out** that might be assets, repairs, or expenses.

| Framework | Primary hooks |
|---|---|
| MPERS | Section 17 *Property, Plant and Equipment*; Section 18 intangibles (`../mpers.md`) |
| MFRS | MFRS 116 PPE; MFRS 138 intangibles (`../mfrs.md`) |

---

## When this checklist fires

- Material bank **debits** that look one-off, equipment-like, renovation, software, vehicles  
- User asks “capitalise or expense?”  
- `classify_depth` = `standards_aware` and material non-routine outflows exist  

Write conclusions to: `workpapers/analysis/capital_vs_expense.md`  
If PPE concluded: also sketch `workpapers/analysis/ppe_and_depreciation.md` (or YE FAR).

---

## Decision tree

### A. Is it even an accounting “purchase”?

| Signal | Likely treatment |
|---|---|
| Owner drawings / personal | Drawings / director current account — not expense of the business if private |
| Loan repayment / principal | Balance sheet (liability) |
| Tax / EPF / SOCSO remittance | Statutory liability clearance or expense per nature |
| Inventory stock purchase | Inventory (asset) then COGS when sold — not always “expense day one” |
| Operating opex (rent, utilities, salaries) | Expense (unless prepaid) |

### B. Capitalise vs expense (PPE / long-lived)

Capitalise when **all** are met (substance over form):

1. **Probable future economic benefits** will flow to the entity  
2. **Cost can be measured reliably** (invoice / contract)  
3. Item is held for use in production/supply/admin (or rental to others / investment property rules)  
4. Meets firm **capitalisation threshold** if set (else use engagement materiality; ask if unsure)

**Expense** (typical):

- Day-to-day repairs and maintenance that only restore existing condition  
- Small tools below threshold  
- Training, most marketing, general admin  

**Grey zone — ask (do not silent-pick aggressive):**

- Major renovation / overhaul that extends useful life or capacity  
- Software (licence vs SaaS subscription)  
- Deposit for equipment not yet received  

### C. After capitalise

- Cost = purchase price + directly attributable costs (delivery, install) — **from sources**  
- Useful life & method: prior year policy > firm default > **ask staff** (never invent rates)  
- Residual value: document if material  
- Depreciation starts when available for use  
- Disposals: remove cost & accum. dep; gain/loss to P&L  

### D. Prepayments

- Payment for future period benefit (insurance, rent) → prepayment asset, release over time  

---

## Outputs required

1. Table of material outflows with capitalise / expense / BS / query  
2. Proposed COA codes  
3. FAR lines to add (if capitalise)  
4. Depreciation policy notes (or “defer to YE — policy TBD”)  
5. Open queries  

---

## Anti-patterns

- Expensing all equipment to “misc expenses” to avoid FAR  
- Capitalising repairs to inflate assets  
- Inventing useful lives or residual values  
- Ignoring owner personal spend on the company card  
