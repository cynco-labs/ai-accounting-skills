---
name: quality-review
description: >
  Prove the pack before finalisation — full QC with Section A mathematical
  blockers. Use when quality review, QC, partner checklist, "check the
  accounts", or prove intent before issue.
---
# /quality-review

## Purpose

Independent checklist pass before anything is called final. Main job: **prove**.

Load `shared/guardrails.md` and execute **every** item in 
`references/qc_checklist.md` (plugin or repo root shim).

## Preconditions

1. Active engagement on disk (`engagement_state.json`).
2. Adjusted TB present when FS claimed — **`roll_tb` derived**, not freestyle.
3. Re-read workpapers/FS if context was compacted (**disk is truth**).

## Steps

### 1 — Section A mathematical integrity [BLOCKERS]

Run every Section A check in `references/qc_checklist.md` against artifacts on disk.

| Check | Pass when |
|---|---|
| TB DR = CR | `tb_adjusted.json` (or claimed TB) difference 0 |
| BS balances | Assets = liabilities + equity |
| P&L ↔ RE | RE movement ties to profit and distributions |
| Each JE balances | Period + YE journals |
| Bank GL = recon | Diff 0.00 per bank or **with limitation** logged |
| Cash flow ↔ cash | Net CF explains cash movement |

**Done when:** every Section A item is Pass, or any Fail is written and finalisation is blocked.

### 2 — Sections B–E

Execute Data integrity, Standards, Completeness, Format from the same checklist. 
Material fails → queries or fix list; do not silent-pass.

**Done when:** every checklist row has Pass / Fail / N/A with evidence path.

### 3 — Report + state

Write QC report under the engagement (e.g. `workpapers/qc_report.md` or firm path). 
Update `engagement_state.json`: prove stage result; **must stop** if any Section A Fail.

**Done when:** report on disk and state reflects pass or blocker.

## Gates

- Any Section A Fail → **cannot finalise** (blocker).
- Provenance gaps on material figures → Fail Section B, not a soft skip.

## Failure modes

| Failure | Behavior |
|---|---|
| Agent scores from memory | Re-open TB / BS / recon files; re-run checks |
| TB freestyled in chat | Reject; require `roll_tb` artifact |
| Premature “QC passed” | Exhaustive bar: every checklist row statused |

## Output

QC report Pass/Fail per item. Next: `finalise-accounts` only if Section A clean (and firm policy).

## Trust surface

Engagement folder + firm config. No external send.
