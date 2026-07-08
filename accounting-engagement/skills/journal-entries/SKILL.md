---
name: journal-entries
description: >
  Build balancing double-entry journals from classified activity and openings.
  Trigger on journals, postings, double entry, JE list, "post the books".
---
# /journal-entries

## Purpose

Convert classified activity into double-entry journals.

## JE packs

1. **JE-001 Opening balances** — from prior year signed FS / TB (highest authority first)
2. **Bank transaction JEs** — one per classified bank line (or batched daily by type if firm policy allows)
3. **Sales/purchase accruals** if invoice books kept on accrual independent of bank
4. **Payroll monthly JEs** — gross + employer statutory; clear net pay / deductions through payables
5. **Client-supplied journals** — re-numbered into sequence with source note

## Format

```
date | je_number | narration | account_code | account_name | debit | credit | source_ref
```

## Validation (blocker)
- Each JE: sum(debit)=sum(credit)
- No one-sided entries
- No blank accounts

## Output
Journals sheet/dataset + imbalance report (must be empty).
