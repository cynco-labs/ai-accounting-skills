---
name: jurisdiction-scaffold
description: >
  Scaffold a new jurisdiction pack under references/jurisdictions/<id>
  without forking stage plugins.
disable-model-invocation: true
argument-hint: "<jurisdiction-id> [--currency CODE] [--framework name]"
---
# /jurisdiction-scaffold

## Purpose

Bootstrap a jurisdiction pack without forking stage plugins.

## Preconditions

Read `shared/jurisdiction-extension-guide.md` and `CONTEXT.md` (**jurisdiction pack** term).

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
7. Remind: paste rates from official sources with retrieval date — do not hard-code from memory

**Done when:** tree exists, every stub has the verify banner, and the contributor has an ordered fill list.

## Output

Tree listing + next actions for the contributor.

## Non-goals

- Does not claim the pack is complete or verified
- Does not modify stage plugin skills beyond pointing at the pack id in firm profile docs if asked
