# reconciliation-accounting

Bank reconciliations and subledger ties (AR, AP, inventory, fixed assets, loans, taxes) culminating in a preliminary trial balance.

## Skills

| Skill | Purpose | Command |
|---|---|---|
| `bank-reconciliation` | Bank recon to RM0 | `/reconciliation-accounting:bank-reconciliation` |
| `subledger-reconciliations` | AR/AP/FA/loans/tax | `/reconciliation-accounting:subledger-reconciliations` |
| `preliminary-trial-balance` | Pre-YE TB | `/reconciliation-accounting:preliminary-trial-balance` |

## Setup

Firm-wide: `/engagement-accounting:cold-start-interview`

Runtime config: `~/.claude/plugins/config/cynco-accounting-skills/reconciliation-accounting/CLAUDE.md`

## Guardrails

See `../shared/guardrails.md`.
