---
name: subledger-reconciliations
description: >
 Reconcile AR/AP and other subledgers to control accounts. Use when AR/AP
 recon or subledgers.
---
# /subledger-reconciliations

## Purpose

Tie subsidiary records to GL control accounts.

## Modules (run all that apply)

### Trade receivables
- Customer listing vs AR control
- Credit balances in AR investigated
- Subsequent receipts / ageing for ECL later

### Trade payables
- Supplier listing vs AP control
- Debit balances in AP investigated
- Unrecorded invoices search (GRNI / statements)

### Inventory
- Stock count / listing vs GL
- Valuation method per policy
- NRV consideration flag for YE

### Fixed assets
- FAR cost & accum dep vs GL
- Additions/disposals completeness vs invoices/bank
- Assets < threshold expensed consistently

### Loans / borrowings
- Lender statement vs GL principal
- Interest accrual vs payments split
- Current vs non-current split for SOFP

### Tax accounts
- Tax payable / recoverable vs notices & CT
- PCB, SST/GST if applicable — separate from income tax

### Payroll liabilities
- EPF/SOCSO/EIS/PCB payables vs payment evidence


## Completion

**Done when:** material subledgers tied or queried; recon notes on disk.

## Output
Recon pack with differences. Material unreconciled items → queries or adjusting JEs (do not hide).
