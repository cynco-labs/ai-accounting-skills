# Malaysia — Revenue recognition checklist (workflow summary)

**Not official MASB text.** Verify against current MPERS / MFRS and engagement facts.  
Use when classifying **material money in** (bank credits, sales receipts).

| Framework | Primary reference in this pack |
|---|---|
| MPERS | Section 23 *Revenue* (`../mpers.md`) |
| MFRS | MFRS 15 *Revenue from Contracts with Customers* (`../mfrs.md`) — five-step model |

---

## When this checklist fires

- Material bank **credits** (customer-like or unexplained)  
- User asks for revenue recognition / sales analysis  
- `classify_depth` = `standards_aware` and money-in themes exist  

Write conclusions to: `workpapers/analysis/revenue_recognition.md`

---

## Decision tree (agent walks this)

### A. Is it revenue at all?

| Question | If yes | If no |
|---|---|---|
| Owner’s capital / director loan in? | Not revenue → equity / liability | Continue |
| Loan drawdown / financing? | Liability | Continue |
| Refund / chargeback / transfer between own accounts? | Contra / clear balance sheet | Continue |
| Customer pays for goods or services? | Continue to B | Query |

### B. MPERS Section 23 (typical Sdn Bhd / SME)

Walk **only** what fits the facts:

1. **Sale of goods** — Have significant risks and rewards of ownership passed to the buyer? Revenue when that happens (often delivery), not merely when cash hits the bank.  
2. **Rendering of services** — Can stage of completion be measured reliably? Recognise by stage; else limited methods / defer.  
3. **Construction / long contracts** — Percentage of completion if criteria met; else careful deferral.  
4. **Interest / royalties / dividends** — Recognise when earned / right to receive, per S23.  
5. **Agency vs principal** — If agent, revenue is **commission only**, not gross receipts.  
6. **Customer advances / deposits** — Cash in may be **contract liability** until performance.  

### C. MFRS 15 (if framework is MFRS)

1. Identify the contract with the customer  
2. Identify performance obligations  
3. Determine transaction price  
4. Allocate price to performance obligations  
5. Recognise revenue when (or as) each obligation is satisfied (point-in-time vs over time)

### D. Cut-off

- Cash received **before** performance → liability / deferred revenue until earned  
- Performance **before** cash → receivable + revenue (if criteria met)  
- Bank date alone is **not** the recognition date  

---

## Outputs required

1. Streams table (customer type / product / service) with amounts tied to sources  
2. Recognition conclusion per stream (when + which COA)  
3. Deferred / deposit balances if any  
4. Open queries for ambiguous contracts  
5. Payee_map updates for confirmed customers  

---

## Anti-patterns

- Coding every bank credit as “Sales” without substance  
- Grossing up agent collections as revenue  
- Ignoring deposits sitting in “Sales”  
- Inventing invoice values not in sources  
