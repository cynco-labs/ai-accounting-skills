# Jurisdiction Extension Guide

How to add a country or reporting regime without forking the marketplace.

## Architecture rule

```
Stage plugins (universal pipeline)
        +
Jurisdiction pack (standards, tax, entities, forms)
        +
Optional industry COA overlays
```

Do **not** create `bookkeeping-accounting-uk` vs `bookkeeping-accounting-my`.  
Do create `references/jurisdictions/uk/` (or `ifrs-sme/`, `us-gaap/`, etc.).

## Pack layout

```
references/jurisdictions/<id>/
  README.md                 # scope, authority sources, version, last verified date
  entity_types.md           # entity → framework → tax form matrix
  financial_reporting.md    # standards map (or mpers.md / ifrs.md)
  tax.md                    # computation outline, rates pointer, forms
  statutory_deductions.md   # payroll withholdings if applicable
  coa/                      # optional entity COA JSON files
  notes-templates/          # optional disclosure scaffolds
  filing_calendar.md        # indicative only — always [verify]
  MANIFEST.json             # machine-readable pack metadata
```

### MANIFEST.json schema

```json
{
  "id": "malaysia",
  "display_name": "Malaysia",
  "currency": "MYR",
  "default_framework": "MPERS",
  "standards_body": "MASB",
  "tax_authority": "LHDN / IRBM",
  "last_verified": "YYYY-MM-DD",
  "files": ["entity_types.md", "mpers.md", "mfrs.md", "tax_malaysia.md"],
  "status": "reference_summary"
}
```

`status` values:

- `reference_summary` — workflow aid; not official text  
- `community` — contributed; needs maintainer review  
- `verified` — maintainer attested last_verified recently  

## Wiring skills to a pack

1. Firm cold-start records `**Jurisdiction pack:** <id>` in firm-profile.
2. Skills load `references/jurisdictions/<id>/` when they need doctrine.
3. If pack missing, skill says so and offers `/accounting-builder-hub:jurisdiction-scaffold`.
4. Keep root `references/*.md` as **compatibility shims** that point to the Malaysia pack until a major version removes them.

## What must stay universal

- Pipeline stage order and gate philosophy (`shared/guardrails.md`)
- Skill names for stages (translate examples, not command names, unless major version)
- Number integrity rules
- Client workspace layout

## What is jurisdiction-specific

- Framework names and disclosure checklists  
- Tax computation steps and forms  
- Payroll statutory schemes  
- Filing deadlines (always verify)  
- Entity law vocabulary (Sdn Bhd vs Ltd vs LLC)  

## Contribution checklist

- [ ] `MANIFEST.json` present with `last_verified`
- [ ] Banner on every standards/tax file: workflow summary; verify against authority
- [ ] No live client data
- [ ] At least one entity COA or mapping note
- [ ] Linked from pack `README.md`
- [ ] `validate_marketplace.py` still passes
- [ ] CHANGELOG entry

## Scaffold command

```text
/accounting-builder-hub:jurisdiction-scaffold <id>
```

Creates the folder skeleton and TODO stubs.
