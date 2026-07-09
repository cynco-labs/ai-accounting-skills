---
name: extract
description: Extract bank statements to proved transaction lines.
disable-model-invocation: true
---
# /extract

Short name for bank / source extraction.

## Do this

1. Load and execute **`extract-bank-statement`**  
   (`bookkeeping-accounting/skills/extract-bank-statement/SKILL.md`).  
2. Prefer CSV; use Maybank adapter for Maybank Islamic PDFs; fail loud on balance breaks.  
3. Write `workpapers/transactions.json` (+ xlsx if requested) and update source register.

**Done when:** extract skill Done when is met.

See `shared/slash-surface.md`.
