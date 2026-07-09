# Shared Guardrails — All Accounting Plugins

Every skill in this marketplace MUST follow these rules. They override convenience.

## Professional responsibility

> **Every output is a draft for accountant / partner review — not signed financial statements, not an audit or review opinion, not tax advice, and not a substitute for a licensed professional.**  
> The reviewing professional verifies figures against source documents, applies judgment, and takes responsibility for anything issued to clients, auditors, registries, or tax authorities.

## Number integrity (non-negotiable)

1. **Never fabricate, estimate, or hallucinate numbers.** Every figure must trace to a source document, prior-year signed accounts, or an explicit formula on source numbers.
2. **If context was compacted or you lost the numbers — re-read the source files.** Do not reconstruct from memory.
3. **Zero tolerance for imbalance.** Trial balance, balance sheet, and each journal entry must balance to the reporting currency’s minor unit (e.g. RM0.00 / $0.00).
4. **Bank must reconcile exactly** (zero difference). Outstanding items must be listed and aged.
5. **Opening balances** must agree to the prior year’s audited/signed closing balances (or documented exceptions).

## Workflow discipline

1. Check documents **before** asking the user. Only ask when genuinely missing or contradictory.
2. **Work the period you have.** Partial months → complete books for that span; do not demand a full year to begin. Label limited period honestly; never invent missing months.
3. **Suspense is last resort.** Auto-classify → ask staff → then suspense + query sheet.
4. Standards and tax compliance are non-negotiable for material items. No silent aggressive positions.
5. Document every classification decision, assumption, and query in working papers / client README.
6. Jurisdiction content is a **workflow summary** — tag `[verify — authoritative source]` for rates, thresholds, and due dates that may change.

## Precision defaults (override in firm profile)

| Item | Default |
|---|---|
| Line-item materiality | Reporting-currency 100 units (group below if immaterial) |
| Rounding | Minor unit (e.g. sen/cents) in workpapers |
| Suspense tolerance | Zero |
| Bank recon tolerance | Zero |
| TB balance tolerance | Zero |

## Output headers

Prepend every deliverable (unless the skill says otherwise). Pick by `operator`:

**owner / bookkeeper (default when no firm profile):**

```
DRAFT — for your review (not signed accounts)
[Entity legal name] · [framework]
Period: [dates on disk]
```

**firm:**

```
DRAFT — for accountant review (not signed accounts)
[Entity legal name] · [framework]
Period: [FY start] to [FY end]
Prepared for: [firm name from profile]
```

Strip this header only when producing client-facing final packs **after** quality review + management approval gates have passed.

## Config paths

| What | Path |
|---|---|
| Firm practice profile | `~/.claude/plugins/config/claude-for-accounting/engagement-accounting/CLAUDE.md` |
| Shared firm facts | `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` |
| Active client workspace | path recorded by engagement-setup / client-workspace |

If firm profile is missing or still has `[PLACEHOLDER]`, skills may run in **provisional mode** with explicit `[PROVISIONAL]` tags — or stop and require `/engagement-accounting:cold-start-interview` (skill-dependent).

## Pipeline order (do not skip gates)

```
Source documents
  → Bookkeeping (record + classify)
  → Bank & ledger reconciliations
  → Preliminary trial balance
  → Year-end adjustments
  → Adjusted trial balance
  → Standards technical review
  → Financial statements + notes
  → Quality review
  → Final signed FS (management approval)
  → Tax computation / statutory filings (from locked figures)
```

A later stage must not run on numbers that failed an earlier **blocker** check, unless the user explicitly overrides and the override is logged.

## Operator lens (who is driving)

Load **`shared/operator-lens.md`**. Same number rules for everyone.

| `operator` | Communication | Draft header default |
|---|---|---|
| **owner** | Plain English only | `DRAFT — for your review` |
| **bookkeeper** | Process-clear; codes OK | `DRAFT — for review` |
| **firm** | Staff = technical; client lists = plain | `DRAFT FOR ACCOUNTANT REVIEW` + firm name |

Do not assume `firm` because the repo is engagement-shaped. Infer or soft-ask once; store on `engagement_state.operator`.

## Communication

- **Progress-gating questions** — use the host **structured user-question tool** (`shared/user-questions.md`). Do not only bury asks in prose or `queries.md`.
- **No homework dumps** — never hand the user a bare “open queries” list. Every material gap is an explained choice with options that update the books.
- **Human pack** — default readable deliverable is **HTML** (`outputs/*_pack.html`), not a stack of `.md` files.
- **To firm staff** (`operator: firm`): technical language — account codes, debit/credit analysis, what is wrong and what is needed.
- **To owner / end client:** plain language — numbered questions, one item each, actionable requests for documents or confirmations.

## White-label

Never hard-code a product vendor or a single firm’s identity into client-facing output. Firm name, registration, footer, and letterhead come from the firm profile written at cold-start.
