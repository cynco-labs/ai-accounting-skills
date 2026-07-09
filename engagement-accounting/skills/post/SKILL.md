---
name: post
description: Post balancing journals and build the trial balance with scripts.
disable-model-invocation: true
---
# /post

Short name for double-entry posting + calculated TB.

## Do this

1. Load and execute **`journal-entries`**  
   (`bookkeeping-accounting/skills/journal-entries/SKILL.md`).  
2. Run `post_journals.py` then `roll_tb.py` — never type TB totals.  
3. If user only needs recon after post, continue to `bank-reconciliation` when they ask.

**Done when:** journal-entries Done when is met (`journals.json` + balanced prelim TB or must stop).

See `shared/slash-surface.md`.
