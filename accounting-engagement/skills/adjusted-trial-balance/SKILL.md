---
name: adjusted-trial-balance
description: >
  DERIVED ONLY — roll adjusted TB from journals + YE journals via roll_tb.py.
  ATB is sole numeric source for FS. Do not freestyle. Kernel intent: post.
  Trigger on adjusted trial balance, ATB, post-adjustment TB, roll ATB.
---
# /adjusted-trial-balance

> **Doctrine deleted.** ATB = `roll_tb(journals.json + journals_ye.json)`.  
> See `shared/kernel-contract.md`.

## Required command

```bash
python3 scripts/roll_tb.py --client-dir <client> --adjusted

# or
npx @cynco/accounting-skills tb <client> --adjusted
```

Writes `workpapers/tb_adjusted.json`. Fail if difference ≠ 0.

## Preconditions

1. Period `journals.json` balanced (from `post_journals.py` or validated pack).  
2. YE pack `journals_ye.json` present (empty `journals: []` only if no AJEs and documented).  
3. Guardrails: never fabricate numbers.

## Next

Standards review → present FS from **this** ATB only (`prepare-primary-statements`).
