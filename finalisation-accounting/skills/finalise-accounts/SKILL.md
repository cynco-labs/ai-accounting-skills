---
name: finalise-accounts
description: >
  Lock the engagement books after QC: freeze ATB and journals, version final FS pack, and record finalisation checklist status.
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

## Output
Finalisation memo + file list.
