---
name: cold-start-interview
description: >
 Firm profile cold-start (not a client dump). Use when set up the firm or
 first install.
argument-hint: "[--redo] [--check-integrations] [--full]"
---
# /cold-start-interview

Configures the firm so every accounting plugin produces **firm-specific, white-label** output.

## Purpose

Interview the accountant/partner and write:

1. `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` — firm facts shared by all plugins 
2. `~/.claude/plugins/config/claude-for-accounting/engagement-accounting/CLAUDE.md` — engagement defaults 

Scaffold: `shared/firm-profile-template.md`. 
**Never invent a firm name** if the user skips — leave `[PLACEHOLDER]` and tag later outputs `[PROVISIONAL]`.

## Check current state

- If firm-profile exists and has no `[PLACEHOLDER]` → skip unless `--redo`
- If paused (`<!-- SETUP PAUSED AT: -->`) → resume
- Else run interview

## Preamble (show first)

> **claude-for-accounting** helps accountants run engagements from source documents through financial statements, QC, and tax handoff. 
> **Every output is a draft for professional review** — not signed FS, not an audit opinion, not tax advice. 
> **2 minutes** captures firm identity, jurisdiction pack, and role. **15 minutes** adds policies, escalation, and house style.

Offer **quick** or **full**.

## Interview

### Part 0 — Firm identity & jurisdiction
- Firm legal name, professional registration, contact
- Who uses this day-to-day (partner / manager / associate / bookkeeper)
- Who signs off final FS and tax
- **Jurisdiction pack** (`malaysia` shipped; others via `/accounting-builder-hub:jurisdiction-scaffold`)
- Reporting currency

### Part 1 — Practice mix
- Entity mix (vocabulary from the jurisdiction pack)
- Default financial reporting framework
- Engagement types (compilation / bookkeeping only / full YE + tax / audit support)
- Typical volume per month
- Common industries (for COA overlay defaults)

### Part 2 — Accounting policies (defaults)
- Capitalisation threshold
- Depreciation method and standard rates by class
- Bank recon: monthly vs YE-only
- Inventory valuation (FIFO / weighted average / other)
- Revenue recognition notes for common client industries
- Related-party disclosure habits

### Part 3 — Quality & escalation
- Materiality defaults
- What always escalates to partner (related parties, going concern, tax disputes, large estimates)
- Client query communication style

### Part 4 — Seed materials (full only)
Ask for 1–2 sample completed working papers or signed FS. Keep seeds **local** — do not commit client data to git.

## Write firm-profile.md

Follow `shared/firm-profile-template.md`. Include jurisdiction pack id, default framework, currency, sign-off rules, and `Updated: [date]`.

Also write engagement-accounting CLAUDE.md from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`.

## `--check-integrations`

Probe connectors per `CONNECTORS.md`. Report ✓ only when a live tool call succeeds. Configured-but-untested → ⚪.

## Close

Summarise what was written. Propose:

1. `/engagement-accounting:engagement-setup` for a live client 
2. Or `/engagement-accounting:full-engagement-pipeline` when documents are ready 

## Tone

Professional colleague onboarding a senior associate — precise, firm-neutral, not salesy.

## Completion

**Done when:** firm-profile written under config path (or user declined) and next engagement path clear.

