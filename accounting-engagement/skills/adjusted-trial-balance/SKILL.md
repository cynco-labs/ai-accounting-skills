---
name: adjusted-trial-balance
description: >
  Derive adjusted TB via roll_tb --adjusted only. Use when adjusted TB or
  ATB.
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


## Completion

**Done when:** `tb_adjusted.json` exists with `difference == 0` via `roll_tb.py --adjusted`.

## Next

Standards review → present FS from **this** ATB only (`prepare-primary-statements`).
