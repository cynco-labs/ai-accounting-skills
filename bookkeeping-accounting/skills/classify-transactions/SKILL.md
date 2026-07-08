---
name: classify-transactions
description: >
  Categorize every transaction to the chart of accounts using prior-year mapping, pattern rules, invoice matching, then employee Q&A. Use after recording transactions.
---

# /classify-transactions

## Purpose

Assign account codes correctly. Accuracy over speed.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/cynco-accounting-skills/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Priority order

### 1. Prior-year payee mapping (returning clients)
Same payee → same account.  
**Flag if amount >30% change** or frequency changed — confirm with employee.

### 2. Pattern rules (Malaysia-aware defaults)

| Pattern | Typical account |
|---|---|
| Salary / wages | 5000 Salary |
| EPF / KWSP remittance | EPF payable / expense split |
| SOCSO / PERKESO | SOCSO payable / expense |
| EIS | EIS payable / expense |
| LHDN / PCB / CP204 | Tax payable / tax expense |
| TNB, SAJ, IWK, TM, Maxis, Celcom, Digi, U Mobile | Utilities |
| Bank charges | Bank charges |
| Interest charged by bank | Finance cost |
| Adobe, Google, Microsoft, Canva, Zoom | Software / subscriptions |
| Rent recurring same amount | Rental expense / prepayment later |
| > RM2,000 asset-like | Consider PPE capitalisation |

Load firm overrides from practice profile.

### 3. Invoice matching
Match amount ± date window to purchase/sales invoices.

### 4. Unclassified → employee batch ask
Group by payee. One question per group with 3–5 account options + “client query / suspense”.

### 5. Suspense (last resort)
Code suspense + add to Queries sheet with exact amount/date/description.

## Output
Transaction register with `account_code`, `account_name`, `classification_basis` (`prior_year|pattern|invoice|employee|suspense`), confidence.

Update client README payee map for next year.
