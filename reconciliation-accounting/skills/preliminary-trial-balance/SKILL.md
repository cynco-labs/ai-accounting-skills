---
name: preliminary-trial-balance
description: >
  DERIVED ONLY — roll preliminary TB from journals via scripts/roll_tb.py.
  Do not freestyle TB totals. Kernel intent: post (see shared/skill-collapse-map.md).
  Trigger on trial balance, TB, pre-adjustment TB, "does the TB balance", roll TB.
---
# /preliminary-trial-balance

> **Doctrine deleted.** Preliminary TB is a pure reduce of `journals.json`.  
> See `shared/kernel-contract.md`.

## Required command

```bash
python3 scripts/roll_tb.py --client-dir <client> --preliminary

# or
npx @cynco/accounting-skills tb <client> --preliminary
```

Writes `workpapers/tb_preliminary.json` with `totals.difference == 0` or fails.

## Forbidden

- Typing TB lines or totals in chat  
- “Balancing figures”  
- Building TB without journals on disk  

## Next

Year-end adjustments → `journals_ye.json` → `roll_tb --adjusted` (ATB for FS).
