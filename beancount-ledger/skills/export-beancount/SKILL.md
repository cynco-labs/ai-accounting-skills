---
name: export-beancount
description: >
  Export balanced journals to Beancount ledger SoR (prove job). Use when
  beancount or export ledger.
---

# /export-beancount

## Purpose

Push **final (or draft-marked) books** into **Beancount** — the ledger system of record.

```text
workpapers/journals*.json + COA → ledger/main.beancount → Fava
```

Excel remains human working papers. **Beancount is where the ledger lives for agents and git.**

Load: `references/beancount_integration.md`

## When

| Situation | Output |
|---|---|
| QC passed / finalise done | `ledger/main.beancount` |
| User wants mid-engagement preview | `ledger/draft.beancount` (label provisional) |
| Unbalanced journals | **Refuse** until fixed |

## Preconditions

1. `workpapers/journals.json` exists (and `journals_ye.json` if YE posted) 
2. Prefer `workpapers/coa.json` or entity COA template 
3. Each JE: sum(debit) = sum(credit) 
4. `pip install beancount` recommended for `--bean-check`

## Command

```bash
python3 scripts/export_to_beancount.py \
 --client-dir "<client_workspace>" \
 --output "<client_workspace>/ledger/main.beancount" \
 --bean-check
```

Or explicit paths:

```bash
python3 scripts/export_to_beancount.py \
 --journals workpapers/journals.json \
 --journals-ye workpapers/journals_ye.json \
 --coa references/coa_templates/coa_sdn_bhd.json \
 --currency MYR \
 --title "LEGAL NAME SDN. BHD." \
 --output ledger/main.beancount \
 --bean-check
```

## What the exporter does

1. Map COA codes → Beancount accounts (`Assets:…`, `Liabilities:…`, `Equity:…`, `Income:…`, `Expenses:…`) 
2. Emit `open` directives 
3. Emit one Beancount transaction per journal entry (DR +, CR −) 
4. Write `*.account_map.json` sidecar 
5. Optional `bean-check` 


## Completion

**Done when:** `ledger/main.beancount` written from balanced journals; refuse if any JE unbalanced.

## Outputs

- `ledger/main.beancount` (or draft path) 
- `ledger/main.beancount.account_map.json` 
- Update `engagement_state.json`: artifact `beancount_ledger`, stage note 

## Next

- `validate-beancount` if check not run 
- `open-fava` to show the user 

## Failure modes

| Issue | Action |
|---|---|
| Unbalanced JE | Stop; fix journals |
| bean-check fail | Show stderr; fix mapping/dates |
| Missing beancount install | `pip install beancount fava` once |
