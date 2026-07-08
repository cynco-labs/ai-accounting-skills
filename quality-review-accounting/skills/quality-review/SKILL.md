---
name: quality-review
description: >
  Full QC including Section A mathematical blockers before finalisation.
  Trigger on quality review, QC, quality control, check the accounts, partner
  review checklist.
---
# /quality-review

## Purpose

Independent checklist pass before anything is called final.

Load `references/qc_checklist.md` and execute **every** section.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Section A — Mathematical integrity [BLOCKERS]
- TB DR=CR
- BS balances
- P&L ↔ RE movement
- Each JE balances
- Bank GL = bank recon
- Cash flow ↔ cash movement

## Section B — Data integrity
Source traceability, openings, dep, payroll, statutory rates.

## Section C — Standards
Framework, accruals, related parties, revenue, leases, impairment, tax link.

## Section D — Completeness
Suspense, accruals, prepayments, bad debts, deliverables, queries, FAR, inventory.

## Section E — Format
House style, name, period, page numbers, comparatives.

## Output
QC report with Pass/Fail per item. Any Section A Fail → **cannot finalise**.
