# Quality Control Checklist

Run this checklist at Phase 6 before generating final outputs. Items marked [BLOCKER] must pass — cannot proceed to output if any fail.

---

## Section A: Mathematical Integrity [ALL BLOCKERS]

| # | Check | Expected | Status |
|---|---|---|---|
| A1 | Trial Balance: Total DR = Total CR | Difference = RM0.00 | |
| A2 | Balance Sheet: Total Assets = Total Liabilities + Total Equity | Difference = RM0.00 | |
| A3 | P&L net profit/loss ties to BS retained earnings movement | Current year RE = Opening RE + Net Profit - Dividends - Drawings | |
| A4 | Every Journal Entry: DR total = CR total | All JEs balance | |
| A5 | Bank GL closing balance = Bank statement closing balance | Per bank account, difference = RM0.00 | |
| A6 | Cash Flow Statement: Net movement = Change in cash & bank | Opening cash + net CF = Closing cash | |

**If any Section A item fails:** STOP. Identify the discrepancy. Trace it to the source journal entry. Fix before proceeding.

---

## Section B: Data Integrity

| # | Check | What to verify |
|---|---|---|
| B1 | No fabricated data | Every number traces to a source document, prior year balance, or explicit calculation |
| B2 | Bank statement extraction complete | First transaction date to last, no gaps in statement coverage |
| B3 | Running balance verified | Bank GL running balance matches bank statement running balance throughout |
| B4 | Opening balances correct | Match prior year closing exactly (audited accounts > management accounts > working papers) |
| B5 | Depreciation calculation accurate | Rate × cost × time proportion = depreciation charge. Verify per asset. |
| B6 | Payroll reconciliation | Total salary per GL = sum of monthly payslips net pay + statutory deductions |
| B7 | Statutory contributions accurate | EPF/SOCSO/EIS at correct rates, correct wage base, within caps |

---

## Section C: Standards Compliance

| # | Check | What to verify |
|---|---|---|
| C1 | Correct framework applied | Entity type → framework (MFRS for Bhd, MPERS for Sdn Bhd/PLT, etc.) |
| C2 | Accrual basis confirmed | Revenue/expenses recognised when earned/incurred, not when cash moves |
| C3 | Depreciation method & rates consistent | Same method/rates as prior year (unless change in estimate documented) |
| C4 | Related party transactions disclosed | Identified all related parties, disclosed material transactions |
| C5 | Director remuneration properly classified | Separate from employee salary, correctly categorised (5035 vs 5000) |
| C6 | Revenue recognition criteria met | Goods: risks/rewards transferred. Services: over time or point in time per framework. |
| C7 | Tax computation links to accounts | Adjusted income starts from P&L net profit. Add-backs tie to GL. |
| C8 | Capital allowances link to asset register | QE per asset = cost per fixed asset register. Rates match asset class. |
| C9 | Lease classification correct | Finance vs operating per S20 criteria (MPERS) or all on BS per MFRS 16 |
| C10 | Impairment considered | Indicators assessed. If indicators exist, recoverable amount tested. |

---

## Section D: Completeness

| # | Check | What to verify |
|---|---|---|
| D1 | All bank transactions classified | No items remain in Suspense (or if any, documented in Queries with justification) |
| D2 | Year-end accruals raised | Audit fees, tax fees, bonus provisions, utility accruals, unbilled revenue |
| D3 | Prepayments identified | Insurance, rent, subscriptions paid in advance → asset (next year portion) |
| D4 | Bad debts assessed | Receivables reviewed for collectability. Specific provision if doubtful. |
| D5 | All deliverables produced | Working papers (Excel) + Financial statements (PDF) + Tax computation |
| D6 | Queries documented | All unresolved items listed with clear question for client/employee |
| D7 | Fixed assets complete | All acquisitions and disposals during year captured |
| D8 | Inventory/COGS (if trading) | Closing stock valued, COGS computed correctly |

---

## Section E: Report Format

| # | Check | What to verify |
|---|---|---|
| E1 | Black & white only | No colour in any output document |
| E2 | Firm branding present | Footer shows firm name and registration on every page (except cover) |
| E3 | Client name correct | Full legal name as per SSM/registration, consistent throughout |
| E4 | FY period stated | "For the financial year ended [date]" or "For the period from [date] to [date]" |
| E5 | Page numbers present | Sequential, in footer |
| E6 | Consistent formatting | Same font, same number formatting (commas, decimals), same column widths |
| E7 | Comparative figures | Prior year shown for all statement items (required for MFRS/MPERS) |

---

## Section F: Edge Cases

| # | Check | What to verify |
|---|---|---|
| F1 | Personal expenses (Sole Prop) | Correctly booked as Drawings, not business expenses |
| F2 | Mixed use assets | Apportioned correctly (e.g., motor vehicle business %) |
| F3 | Employer absorption | If employer absorbs employee statutory, full amount in employer expense |
| F4 | Director vs Employee | Correctly classified, correct statutory treatment |
| F5 | Capital vs Revenue | Items > RM2,000 capitalised, items < RM2,000 expensed or 100% CA |
| F6 | Inter-entity transactions | Identified, disclosed, arm's length pricing considered |
| F7 | Foreign currency | Monetary items at closing rate, exchange differences in P&L |
| F8 | Pro-rated depreciation | New acquisitions depreciated from acquisition date (not full year) |
| F9 | HP assets | Full cost capitalised (not just payments made), interest allocated over term |
| F10 | GST/SST | If registered, output tax correctly accounted; input tax claimed or expensed |

---

## QC Report Format

After running all checks, produce a summary:

```
QUALITY CONTROL REPORT
Client: [Name]
FY: [Period]
Date: [Processing Date]
Prepared by: [Agent/Employee]

SECTION A (Mathematical Integrity): [PASS/FAIL]
  A1: [PASS] TB balanced at RM XXX
  A2: [PASS] BS balanced at RM XXX
  ...

SECTION B (Data Integrity): [X/7 passed]
  [List any failures with explanation]

SECTION C (Standards Compliance): [X/10 passed]
  [List any failures with explanation]

SECTION D (Completeness): [X/8 passed]
  [List any failures with explanation]

SECTION E (Report Format): [X/7 passed]
  [List any failures with explanation]

SECTION F (Edge Cases): [X/10 applicable, X passed]
  [List any failures with explanation]

OVERALL: [PASS / PASS WITH NOTES / FAIL]
[If FAIL: list blockers that must be resolved]
[If PASS WITH NOTES: list items for attention/disclosure]
```
