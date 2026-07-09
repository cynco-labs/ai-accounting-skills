---
name: prepare-primary-statements
description: >
 Present primary statements from ATB map (present job). Use when draft
 FS or SOFP/SOCI.
---
# /prepare-primary-statements

## Purpose

Map ATB → primary statements under the engagement framework.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Statements

1. **Statement of Financial Position** (SOFP) — current/non-current split (MPERS S4)
2. **Statement of Comprehensive Income** — single-statement or two-statement (S5)
3. **Statement of Changes in Equity** (S6)
4. **Statement of Cash Flows** — indirect (default) or direct (S7)

## Mapping rules
- Maintain explicit **ATB code → FS line** map; every ATB balance appears exactly once in SOCI or SOFP (except zero).
- Comparatives from prior signed FS (not memory).
- Rounding to nearest ringgit only if firm policy says so; default sen precision in workpapers, presentation per house style.

## Cash flow ties
Net change in cash = SOFP cash movement. Reconcile profit to operating cash.

## Checks before handoff
- Assets = Liabilities + Equity
- SOCI result feeds equity (RE / current year result)
- No unexplained “balancing figures”


## Completion

**Done when:** primaries on disk map to ATB lines, BS balances, and figures carry provenance tags.

## Output
Primary statements draft + mapping schedule. Next: `prepare-notes`.
