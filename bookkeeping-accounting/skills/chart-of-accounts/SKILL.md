---
name: chart-of-accounts
description: >
  Select, customise, and maintain the chart of accounts for the entity type (Sdn Bhd, sole prop, PLT, etc.). Use when setting up books or adding accounts.
---

# /chart-of-accounts

## Purpose

Ensure the COA fits entity type and reporting needs.

## Templates
Load from `references/coa_templates/`:
- `coa_sdn_bhd.json`, `coa_bhd.json`, `coa_plt.json`, `coa_sole_prop.json`, `coa_partnership.json`, `coa_koperasi.json`

## Rules
1. Prefer template codes for consistency across firm clients.
2. Add sub-accounts only when reporting/analysis needs it.
3. Never reuse a code for a different nature (asset vs expense).
4. Map every FS line item to one or more codes (maintain mapping table for statements skill).
5. Suspense account required (e.g. 2900).

## Output
Active COA list + FS mapping skeleton (code → SOFP/SOCI line).
