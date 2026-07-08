---
name: cold-start-interview
description: >
  Run the firm cold-start interview to write firm-profile.md and the engagement practice profile. Use on first install, when config has [PLACEHOLDER], or when the user says set up the firm, configure accounting plugins, or onboard me.
---

# /cold-start-interview

Configures the firm so every accounting plugin produces firm-specific output.

## Purpose

Interview the accountant/partner and write:

1. `~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md` — firm facts shared by all plugins
2. `~/.claude/plugins/config/cynco-accounting-skills/engagement-accounting/CLAUDE.md` — engagement defaults

## Check current state

- If firm-profile exists and has no `[PLACEHOLDER]` → skip unless `--redo`
- If paused (`<!-- SETUP PAUSED AT: -->`) → resume
- Else run interview

## Interview (quick ~2 min or full ~15 min)

Offer **quick** or **full**.

### Part 0 — Firm identity
- Firm legal name, registration (MIA/CA number), contact email/phone
- Who uses this day-to-day (partner / manager / associate / bookkeeper)
- Who signs off final FS and tax

### Part 1 — Practice mix
- Entity mix (Sdn Bhd / sole prop / PLT / Bhd / other)
- Default framework (usually MPERS for private companies)
- Engagement types (compilation / bookkeeping only / full YE + tax / audit support)
- Typical volume per month

### Part 2 — Accounting policies (defaults)
- Capitalisation threshold (default RM2,000)
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
Ask for 1–2 sample completed working papers or signed FS (redacted ok) to learn house format.

## Write firm-profile.md

```markdown
# Firm Profile — Cynco Accounting Skills

**Firm name:** ...
**Registration:** ...
**Contact:** ...
**Default framework:** MPERS
**Currency:** MYR
**Capitalisation threshold:** RM2,000
**Partner sign-off:** ...
**Updated:** [date]
```

Also write the engagement-accounting CLAUDE.md from the template at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`.

## Close

Summarise what was written. Propose:
1. `/engagement-accounting:engagement-setup` for a live client
2. Or `/engagement-accounting:full-engagement-pipeline` when documents are ready

## Tone

Professional colleague onboarding a senior associate — precise, not chatty.
