# Cookbook: Filing deadline watcher

## Purpose

Produce a weekly digest of clients approaching tax or statutory filing windows so nothing slips.

## Security tier

**Read-only** — reads engagement READMEs; writes a digest file or posts to an internal channel if messaging MCP is connected.

## Inputs

- `~/.claude/plugins/config/claude-for-accounting/clients/*/README.md` (or firm-configured client root)
- Fields: legal name, FYE, tax form, FS status (`draft|locked|issued`), tax status (`not_started|draft|filed`)

## Procedure

1. Enumerate active clients.
2. For each, compute indicative windows from jurisdiction pack `filing_calendar.md` if present.
3. **Always** mark dates `[verify — confirm with current tax authority / registry guidance]`.
4. Flag clients with `FS status != issued` but tax window < 60 days.
5. Flag open material queries that block finalisation.
6. Emit digest markdown (and optional Slack post if connected **and** firm profile allows).

## Outputs

`deadlines/digest-YYYY-MM-DD.md`

## Non-goals

- Does not file returns
- Does not email clients
- Does not invent due dates from model memory as hard law

## Skill reuse

- `finalisation-accounting/agents/filing-deadline-watcher.md`
- Jurisdiction pack calendar files when available
