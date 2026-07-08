# Quick Start — Cynco Accounting Skills

Install in about 60 seconds, configure the firm in 2–15 minutes, run an engagement.

## 1. Install marketplace

### Claude Code

```bash
# From this repo path
/plugin marketplace add /Applications/Apps-Hazli/cynco-accounting-skills

# Install the plugins you need (engagement is required; others as needed)
/plugin install engagement-accounting@cynco-accounting-skills
/plugin install bookkeeping-accounting@cynco-accounting-skills
/plugin install reconciliation-accounting@cynco-accounting-skills
/plugin install year-end-accounting@cynco-accounting-skills
/plugin install mpers-accounting@cynco-accounting-skills
/plugin install financial-statements-accounting@cynco-accounting-skills
/plugin install quality-review-accounting@cynco-accounting-skills
/plugin install finalisation-accounting@cynco-accounting-skills
/plugin install tax-accounting@cynco-accounting-skills
```

Or install only the orchestrator path first:

```bash
/plugin install engagement-accounting@cynco-accounting-skills
# install the rest when the pipeline reaches that stage
```

### As a single legacy skill (optional)

The older monolithic skill still lives at `~/.claude/skills/accounting-skills/`. This marketplace **supersedes** it with stage plugins; keep the old skill only if you need the single-file workflow.

## 2. Firm cold-start (do this first)

```text
/engagement-accounting:cold-start-interview
```

Writes:

- `~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md`
- `~/.claude/plugins/config/cynco-accounting-skills/engagement-accounting/CLAUDE.md`

Without this, outputs are generic or tagged `[PROVISIONAL]`.

## 3. Open an engagement

```text
/engagement-accounting:engagement-setup
```

You will identify entity type, FY, framework (MPERS/MFRS/…), and document completeness.

## 4. Run the full pipeline (or stage-by-stage)

**Full pipeline:**

```text
/engagement-accounting:full-engagement-pipeline
```

**Stage-by-stage (recommended for first clients):**

```text
/engagement-accounting:source-documents
/bookkeeping-accounting:record-transactions
/bookkeeping-accounting:classify-transactions
/reconciliation-accounting:bank-reconciliation
/reconciliation-accounting:subledger-reconciliations
/reconciliation-accounting:preliminary-trial-balance
/year-end-accounting:year-end-adjustments
/year-end-accounting:adjusted-trial-balance
/mpers-accounting:mpers-technical-review
/financial-statements-accounting:prepare-primary-statements
/financial-statements-accounting:prepare-notes
/quality-review-accounting:quality-review
/finalisation-accounting:finalise-accounts
/tax-accounting:tax-computation
```

## 5. What “done” looks like

- Balanced adjusted trial balance (DR = CR)
- Balance sheet balances
- Bank recon to RM0.00
- MPERS technical issues cleared or disclosed
- Primary statements + notes consistent
- QC checklist Section A all pass
- Management approval recorded
- Tax computation ties to final P&L (if in scope)

## Guardrails in one line

**Never invent numbers. Never ship an unbalanced TB. Always re-read sources if context is lost.**
