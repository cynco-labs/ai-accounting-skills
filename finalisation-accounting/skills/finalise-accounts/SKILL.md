---
name: finalise-accounts
description: >
 Lock pack after QC pass (prove job). Use when finalise or lock accounts.
---
# /finalise-accounts

## Purpose

Move from draft to **locked** numbers.

## Preconditions
- QC Section A all pass
- Open client queries either cleared or accepted as limitations in report
- MPERS technical issues cleared or disclosed

## Steps
1. Freeze journal sequence (no further posts without re-opening + re-QC)
2. Stamp version: `FS_final_draft_vN` → `FS_for_management_approval`
3. Archive workpapers hash/date
4. Update engagement README status: `LOCKED_PENDING_APPROVAL`
5. **Push system of record (Beancount)** — after lock:
 ```bash
 python3 scripts/export_to_beancount.py \
 --client-dir <client> \
 --output <client>/ledger/main.beancount \
 --bean-check
 ```
 Excel/openpyxl workpapers stay as engagement packs. **Beancount is the ledger SoR.** 
 Offer `open-fava` so the user can browse in the browser (`http://127.0.0.1:5000`). 
 See `references/beancount_integration.md` and skills `export-beancount` / `open-fava`.


## Completion

**Done when:** QC Section A clear (or user-stopped with limitation), lock recorded in state, journals frozen for issue path.

## Output
Finalisation memo + file list + path to `ledger/main.beancount` when exported.
