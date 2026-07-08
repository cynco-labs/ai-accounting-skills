---
name: capital-allowances
description: >
  Compute Malaysian capital allowances (initial and annual) from the fixed asset register, including b/f and c/f residual expenditure.
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

## Output
CA schedule by asset pool/class + total IA/AA for the year.
