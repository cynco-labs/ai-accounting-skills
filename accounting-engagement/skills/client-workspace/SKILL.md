---
name: client-workspace
description: >
  Scaffold clients/<slug> folder layout. Use when new client folder or
  workspace layout. Also the shelf step: organize scattered docs by entity
  and period before extract (see shared/shelf-first.md).
---
# /client-workspace

## Purpose

Keep client work **isolated, path-addressable, and bookkeeper-shaped**.  
**Organize (shelf) before extract.** Doctrine: `shared/shelf-first.md`.

## When to run

- New job / messy folder dump / user pastes many paths  
- User: “organize these files”, “set up the client folder”  
- Before extract when files are not already under `clients/<slug>/source/`

If `engagement_state.json` exists and layout is already standard → only refresh register / add new files.

## Default layout (one job)

```text
{workspace}/clients/{client-slug}/
  README.md
  engagement_state.json
  source/
    register.md
    inbox/          # optional unsorted arrivals
    bank/
    sales/
    purchases/
    payroll/
    statutory/
    prior/
    other/
    _pointers.md    # optional: originals not copied
  workpapers/
  outputs/
  ledger/
  queries.md
```

Config path alternative: `~/.claude/plugins/config/claude-for-accounting/clients/<slug>/`

## Workflow (shelf-first)

1. **Discover** — cwd + user-mentioned paths (do not scan whole home).  
2. **Inventory** — kind + period + entity guess (`shared/shelf-first.md`).  
3. **Job map** — if multi-entity, table + soft-confirm which job now.  
4. **Scaffold** — create layout for active slug.  
5. **Place** — copy (default) or pointer into `source/<kind>/`; never delete originals.  
6. **Register** — write `source/register.md` + coverage matrix.  
7. Hand off to **smart-intake** / extract for that shelf only.

## Commands (natural language)

- **create** `<name>` — slugify, scaffold folders, seed README  
- **shelf** / **organize** — discover + place + register (this skill’s main path)  
- **switch** `<slug>` — set active client  
- **status** — active client, FY, stage, open queries  
- **list** — known clients under `clients/`

## Rules

- Never mix two clients’ numbers in one workbook without an explicit multi-entity job.  
- Cross-client context is **off** by default.  
- Record the active path so later skills write to the right place.  
- Extract/classify/post only from the active job’s shelf (or registered pointers).

## Completion

**Done when:** standard dirs exist; sources are under `source/**` (or `_pointers.md`); `source/register.md` present; active slug clear.
