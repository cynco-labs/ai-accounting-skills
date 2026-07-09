---
name: capital-allowances
description: >
  Capital allowances schedule from FAR (IA/AA). Use when capital
  allowances or plant allowance.
---
# /capital-allowances

## Purpose

CA schedule for tax computation.

## Inputs
FAR: date, cost, class, residual expenditure b/f, disposals.

## Rules
- Use rates from `references/tax_malaysia.md` (verify currency of rates)
- Small value assets per current rules / firm policy
- Hire purchase: qualifying expenditure rules
- Disposals: balancing charge/allowance


## Completion

**Done when:** CA schedule by pool/class on disk; rates from tax reference (not invented).

## Output
CA schedule by asset pool/class + total IA/AA for the year.
