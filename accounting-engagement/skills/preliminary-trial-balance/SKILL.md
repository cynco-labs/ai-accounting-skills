---
name: preliminary-trial-balance
description: >
  Derive preliminary TB via roll_tb only . Use when preliminary TB
  or roll TB.
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


## Completion

**Done when:** `tb_preliminary.json` exists with `difference == 0` via `roll_tb.py` — never freestyle totals.

## Next

Year-end adjustments → `journals_ye.json` → `roll_tb --adjusted` (ATB for FS).
