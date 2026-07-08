---
name: jurisdiction-scaffold
description: >
  Create a new jurisdiction pack skeleton under references/jurisdictions/<id>
  with MANIFEST, README, and stub doctrine files. Use when adding a country or
  reporting regime to claude-for-accounting.
argument-hint: "<jurisdiction-id> [--currency CODE] [--framework name]"
---

# /jurisdiction-scaffold

## Purpose

Bootstrap a jurisdiction pack without forking stage plugins.

## Preconditions

Read `shared/jurisdiction-extension-guide.md`.

## Inputs

- `id` — lowercase slug (`uk`, `singapore`, `australia`, `ifrs-sme`)
- Optional currency, default framework name

## Steps

1. Create `references/jurisdictions/<id>/`
2. Write `MANIFEST.json` with `status: community`, `last_verified` today, empty files list to fill
3. Write `README.md` with authority sources table (TODO links)
4. Create stubs:
   - `entity_types.md`
   - `financial_reporting.md`
   - `tax.md`
   - `statutory_deductions.md` (if payroll exists)
   - `filing_calendar.md` (all rows `[verify]`)
   - `notes-templates/` (optional empty)
   - `coa/` (optional empty)
5. Banner every stub: workflow summary; not official text
6. Tell the user what to fill first (entity matrix → reporting → tax)
7. Remind: do not hard-code rates from memory; paste from official sources with retrieval date

## Output

Tree listing + next actions for the contributor.

## Non-goals

- Does not claim the pack is complete or verified
- Does not modify stage plugin skills beyond pointing at the pack id in firm profile docs if asked
