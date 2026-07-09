---
name: present
description: Present primary statements (balance sheet / P&L) from the adjusted TB.
disable-model-invocation: true
---
# /present

Short name for statement presentation.

## Do this

1. Load and execute **`prepare-primary-statements`**.  
2. If notes/disclosures needed in the same ask, continue with **`prepare-notes`**.  
3. Optional: `generate-workbook`, `compilation-report` when requested.  
4. Numbers map from **adjusted TB** (`roll_tb --adjusted`) — no freestyle totals.

**Done when:** primaries on disk (and notes if in scope) with sources/ties.

See `shared/slash-surface.md`.
