---
name: preliminary-trial-balance
description: >
  Produce preliminary trial balance before year-end adjustments; require DR=CR.
  Trigger on trial balance, TB, pre-adjustment TB, "does the TB balance".
---
# /preliminary-trial-balance

## Purpose

Snapshot of books **before** YE adjustments.

## Columns
`code | name | opening_dr | opening_cr | movement_dr | movement_cr | closing_dr | closing_cr`

Or firm standard: opening / period / closing with natural balance.

## Checks (blockers)
- Total DR = Total CR
- Bank GL = recon result
- No orphan codes
- Suspense listed if any

## Output
Preliminary TB artifact + “ready for year-end adjustments” flag.  
Next: `/year-end-accounting:year-end-adjustments`
