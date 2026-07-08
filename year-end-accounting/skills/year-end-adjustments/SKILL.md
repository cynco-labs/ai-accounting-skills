---
name: year-end-adjustments
description: >
  Post year-end adjusting journals: depreciation, amortisation, accruals, prepayments, inventory, ECL/bad debts, interest, payroll, tax provision, FX, deferred tax if applicable.
---

# /year-end-adjustments

## Purpose

Accrual-basis completeness at reporting date.

Load and tick `references/year_end_adjustments_checklist.md` (plugin or repo root).

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Adjustment catalogue (evaluate each)

| Adj | Typical DR | Typical CR | Evidence |
|---|---|---|---|
| Depreciation | Dep exp | Accum dep | FAR × rates × time |
| Amortisation | Amort exp | Accum amort | Intangible register |
| Accrued expenses | Expense | Accruals | Invoices after YE, contracts |
| Prepayments | Prepayments | Expense | Insurance/rent/subs |
| Deferred income | Revenue | Deferred income | Amounts received not earned |
| Inventory | Inventory / COGS | COGS / Inventory | Stock count & valuation |
| ECL / bad debts | Impairment exp | Allowance | Ageing + specific ID |
| Interest accrual | Finance cost | Interest payable | Loan schedule |
| Payroll accrual | Salary / bonus | Accruals | Unpaid days, bonus policy |
| Tax provision | Tax expense | Tax payable | Draft tax computation |
| FX retranslation | FX loss/gain | Monetary BS items | Closing rate |
| Deferred tax | Tax exp / DTA | DTL / tax exp | Temporary differences (if material & framework) |
| Related party | per nature | per nature | Confirmations / agreements |

## Rules
1. Each adj is a numbered YE JE with narration and evidence ref.
2. Do not double-count items already correctly accrued in monthly books.
3. Tax provision may be **iterative** with `/tax-accounting:tax-computation` — document version.
4. Material estimates: document assumption; escalate if judgment-heavy.

## Output
YE adjustment journal pack + impact on profit.
