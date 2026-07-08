---
name: client-workspace
description: >
  Create or switch client workspace folders and active client pointer. Trigger
  on new client folder, switch client, list clients, where are workpapers.
---
# /client-workspace

## Purpose

Keep client work isolated and path-addressable.

## Default layout

```
{workspace}/clients/{client-slug}/
  README.md                 # engagement decisions
  source/                   # original docs (or pointers)
  workpapers/
    journals.csv | json
    trial_balance.xlsx
    reconciliations/
  outputs/
    financial_statements/
    tax/
  queries.md
```

Config path alternative: `~/.claude/plugins/config/claude-for-accounting/clients/<slug>/`

## Commands (natural language)

- **create** `<name>` — slugify, scaffold folders, seed README from template
- **switch** `<slug>` — set active client in engagement CLAUDE.md `## Active client`
- **status** — show active client, FY, pipeline stage, open queries
- **list** — list known clients

## Rules

- Never mix two clients' numbers in one workbook without explicit multi-entity consolidation engagement.
- Cross-client context is **off** by default.
- Record the active path so later skills write to the right place.
