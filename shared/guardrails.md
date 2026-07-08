# Shared Guardrails — All Accounting Plugins

Every skill in this marketplace MUST follow these rules. They override convenience.

## Professional responsibility

> **Every output is a draft for accountant / partner review — not signed financial statements, not tax advice, and not a substitute for a licensed professional.**  
> The reviewing accountant verifies figures against source documents, applies professional judgment, and takes responsibility for anything issued to clients, auditors, SSM, or LHDN.

## Number integrity (non-negotiable)

1. **Never fabricate, estimate, or hallucinate numbers.** Every figure must trace to a source document, prior-year signed accounts, or an explicit formula on source numbers.
2. **If context was compacted or you lost the numbers — re-read the source files.** Do not reconstruct from memory.
3. **Zero tolerance for imbalance.** Trial balance, balance sheet, and each journal entry must balance to RM0.00 difference.
4. **Bank must reconcile exactly** (RM0.00). Outstanding items must be listed and aged.
5. **Opening balances** must agree to the prior year's audited/signed closing balances (or documented exceptions).

## Workflow discipline

1. Check documents **before** asking the user. Only ask when genuinely missing or contradictory.
2. **Suspense is last resort.** Auto-classify → ask employee → then suspense + query sheet.
3. Standards compliance is non-negotiable (MPERS / MFRS / ITA 1967). No shortcuts for material items.
4. Document every classification decision, assumption, and query in working papers / client README.

## Precision defaults

| Item | Threshold |
|---|---|
| Line-item materiality (default) | RM100 (group below if immaterial) |
| Rounding | 2 decimal places (sen) throughout |
| Suspense tolerance | RM0.00 |
| Bank recon tolerance | RM0.00 |
| TB balance tolerance | RM0.00 |

Firm-specific materiality overrides live in the firm practice profile (`CLAUDE.md` config).

## Output headers

Prepend every deliverable (unless the skill says otherwise):

```
DRAFT FOR ACCOUNTANT REVIEW — NOT SIGNED FINANCIAL STATEMENTS
Prepared under [MPERS|MFRS|other] for [entity legal name]
Period: [FY start] to [FY end]
Firm: [from practice profile]
```

Strip this header only when producing client-facing final packs **after** quality review + management approval gates have passed.

## Config paths

| What | Path |
|---|---|
| Firm practice profile | `~/.claude/plugins/config/cynco-accounting-skills/engagement-accounting/CLAUDE.md` |
| Shared firm facts | `~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md` |
| Active client workspace | path recorded in engagement setup / client-workspace skill |

If firm profile is missing or still has `[PLACEHOLDER]`, skills may run in **provisional mode** with explicit `[PROVISIONAL]` tags — or stop and require `/engagement-accounting:cold-start-interview` (skill-dependent).

## Pipeline order (do not skip gates)

```
Source documents
  → Bookkeeping (record + classify)
  → Bank & ledger reconciliations
  → Preliminary trial balance
  → Year-end adjustments
  → Adjusted trial balance
  → MPERS / standards technical review
  → Financial statements + notes
  → Quality review
  → Final signed FS (management approval)
  → Tax computation / statutory filings (from locked figures)
```

A later stage must not run on numbers that failed an earlier **blocker** check, unless the user explicitly overrides and the override is logged.

## Communication

- **To firm staff:** technical language — account codes, DR/CR analysis, what is wrong and what is needed.
- **To client:** plain English — numbered questions, one item each, actionable ("Please provide invoice for RM3,800 payment to KENZ DIGITAL on 15/06/2024").
