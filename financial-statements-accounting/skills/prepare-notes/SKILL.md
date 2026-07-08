---
name: prepare-notes
description: >
  Draft notes to the financial statements from MPERS templates, tied to
  primaries. Trigger on notes to accounts, notes to financial statements,
  accounting policies note, PPE note, related party note.
---
# /prepare-notes

## Purpose

Notes are often the longest part — be complete and **tied to primaries**.

## Templates (load these)

For MPERS engagements, load scaffolds from:

`references/notes-templates/mpers/` (see `00_index.md`)

| Order | Template |
|---|---|
| 1 | `01_corporate_information.md` |
| 2 | `02_basis_of_preparation.md` |
| 3 | `03_significant_accounting_policies.md` |
| 4 | `04_critical_judgements.md` |
| 5+ | PPE, receivables, payables, borrowings, revenue, employee benefits, equity, cash |
| End | Related parties, commitments/contingencies, subsequent events |

For other jurisdictions, load `references/jurisdictions/<id>/notes-templates/` if present; otherwise adapt MPERS scaffolds and label framework differences.

## Structure (typical MPERS set)

1. Corporate information  
2. Basis of preparation  
3. Significant accounting policies  
4. Critical accounting estimates  
5–N. Note-by-note breakdowns matching SOFP/SOCI lines  
Final: Related parties, commitments, contingencies, events after reporting period, authorisation  

## Tie rules
- Note totals = primary statement lines
- PPE note rolls cost & accum dep to SOFP carrying amount
- Borrowings note current/non-current split = SOFP
- Related party note includes directors' remuneration where required
- **Every filled amount cites ATB code, schedule, or prior signed FS** — never invent

## Sources
ATB, FAR, loan schedules, MPERS technical review findings, prior year notes (update, don't copy blindly).

## Completeness
After drafting, run or mirror `/mpers-accounting:disclosure-checklist`.

## Output
Full notes draft + cross-ref index (Note # ↔ FS line) + list of notes still `[PENDING source]`.
