---
name: full-engagement-pipeline
description: >
  Orchestrate the full Malaysian accounting engagement from source documents through QC and finalisation (and optional tax). Use when the user wants end-to-end year-end or compilation processing.
---

# /full-engagement-pipeline

## Purpose

Run the engagement pipeline **in order**, stopping on blockers, invoking stage logic equivalent to each plugin skill.

## Pipeline stages (mandatory order)

| # | Stage | Skill equivalent | Gate |
|---|---|---|---|
| 0 | Engagement setup | engagement-setup | Entity + FY known |
| 1 | Source documents | source-documents | Banks complete or override |
| 2 | Record transactions | record-transactions | Extracted |
| 3 | Classify | classify-transactions | No silent suspense |
| 4 | Journals | journal-entries | Each JE balances |
| 5 | Bank recon | bank-reconciliation | RM0.00 |
| 6 | Subledgers | subledger-reconciliations | Material ties done |
| 7 | Preliminary TB | preliminary-trial-balance | DR=CR |
| 8 | YE adjustments | year-end-adjustments | Posted |
| 9 | ATB | adjusted-trial-balance | DR=CR |
| 10 | MPERS review | mpers-technical-review | Issues cleared/disclosed |
| 11 | Primary FS | prepare-primary-statements | BS balances |
| 12 | Notes | prepare-notes | Notes ↔ primary |
| 13 | QC | quality-review | Section A pass |
| 14 | Finalise | finalise-accounts | Partner/management gates |
| 15 | Tax (if in scope) | tax-computation | Ties to locked P&L |

## Orchestration rules

1. At each stage, **load that stage's SKILL.md** from the corresponding plugin (if installed) and follow it fully.
2. If a plugin is not installed, use inlined stage procedures from this skill + repo `references/`.
3. **Stop on Section A / bank / TB blockers.** Present the failure, fix path, and wait.
4. Batch employee classification questions (AskUserQuestion) rather than one-by-one spam.
5. Write intermediate artifacts to the client workspace after each stage.
6. Produce a **pipeline status board** after each stage:

```markdown
| Stage | Status | Artifact | Notes |
|---|---|---|---|
| 5 Bank recon | ✅ | recon_maybank.md | Diff RM0.00 |
| 6 Subledgers | 🟡 | ... | AP unmatched 3 invoices |
```

7. End with next-step tree: issue draft FS / run tax / send management approval pack / open queries to client.

## Scope flags

Ask once at start (or read engagement README):
- Compilation only vs bookkeeping-only vs full YE + tax
- Framework override
- Skip tax? Skip notes (management accounts only)?

Default: **full YE + notes + QC**; tax if Form type known.

## Non-negotiable

Same as `shared/guardrails.md`. This orchestrator does **not** get a free pass to invent numbers for speed.
