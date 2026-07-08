---
name: record-transactions
description: >
  Extract and record all transactions from source documents into structured books — sales, purchases, receipts, payments — with source provenance. Use when bank statements or books need capturing.
---

# /record-transactions

## Purpose

Produce a complete transaction register from source documents with **source links**.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/cynco-accounting-skills/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Streams

### A. Bank / cash receipts & payments
For every bank line:
`date | description | amount | DR/CR | bank_account | source_file | source_page_or_row | running_balance`

Verify:
- Opening = prior closing (or zero)
- Closing = statement closing
- Running balance unbroken

### B. Sales (if invoices provided)
`invoice_no | date | customer | amount | tax | revenue_type | source`

### C. Purchases
`invoice_no | date | supplier | amount | tax | expense_or_asset | source`

### D. Payroll (if payslips)
Monthly: gross, allowances, employee deductions, employer statutory, net pay.  
Check net ↔ bank payment.

### E. Manual journals already provided by client
Record as-is; mark `source=client_journal`; do not “fix” silently.

## Output

Structured dataset (CSV/JSON/workpaper sheet) ready for classification.  
**Do not classify here** unless user asked for combined pass — prefer handoff to `classify-transactions`.

## Failures
Missing months → STOP or log AMBER limitation. Never interpolate missing bank activity.
