---
name: adjusted-trial-balance
description: >
  Generate the adjusted trial balance after all year-end adjustments. This is the single source for financial statement preparation.
---

# /adjusted-trial-balance

## Purpose

**ATB = source of truth for FS mapping.**

## Build
Preliminary TB + all YE JEs (and any post-recon corrections).

## Checks (blockers)
- DR = CR exactly
- P&L nets to a single current-year result account or is clear for SOCI mapping
- No suspense unless disclosed limitation (prefer zero)
- Opening equity agrees to prior year signed FS

## Output
ATB with columns: unadjusted | adjustments | adjusted.  
Next: `/mpers-accounting:mpers-technical-review` then FS skills.
