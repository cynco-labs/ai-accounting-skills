---
name: chart-of-accounts
description: >
  Select entity COA and optional industry overlay. Use when COA setup, add
  account, or industry accounts.
---
# /chart-of-accounts

## Purpose

Ensure the COA fits entity type and reporting needs.

## Templates

### Entity base COAs
Load from `references/coa_templates/` (Malaysia pack defaults):
- `coa_sdn_bhd.json`, `coa_bhd.json`, `coa_plt.json`, `coa_sole_prop.json`, `coa_partnership.json`, `coa_koperasi.json`

Other jurisdictions: `references/jurisdictions/<id>/coa/`.

### Industry overlays (optional)
Merge from `references/coa_templates/industry/` after the entity base:

| Pack | Use when |
|---|---|
| `trading.json` | Merchandise wholesale/retail |
| `services.json` | Professional / agency services |
| `fnb.json` | Food & beverage |
| `property.json` | Investment property / rental |
| `construction.json` | Contracting |

Overlay `overlay_accounts` win on intentional renames; document merges in client README.

## Rules
1. Prefer template codes for consistency across firm clients.
2. Add sub-accounts only when reporting/analysis needs it.
3. Never reuse a code for a different nature (asset vs expense).
4. Map every FS line item to one or more codes (maintain mapping table for statements skill).
5. Suspense account required (e.g. 2900).
6. White-label: no firm-specific account names in shared templates.


## Completion

**Done when:** active COA list on disk (entity base ± overlay) with suspense code and FS mapping skeleton.

## Output
Active COA list + industry overlay applied (if any) + FS mapping skeleton (code → SOFP/SOCI line).
