# Full Engagement Pipeline — Skill Routing

Use this as the canonical stage map. The orchestrator skill
`/engagement-accounting:full-engagement-pipeline` follows the same order.

**Kernel (first principles):** `shared/kernel-contract.md` · collapse map: `shared/skill-collapse-map.md`.  
**TB:** always `scripts/roll_tb.py` (never freestyle).

```
┌──────────────────────┐
│ 1. Source Documents  │  engagement-accounting:source-documents
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. Bookkeeping       │  bookkeeping-accounting:record-transactions
│    Sales / Purchases │  bookkeeping-accounting:classify-transactions
│    Receipts/Payments │  bookkeeping-accounting:journal-entries
│    Journals          │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. Reconciliations   │  reconciliation-accounting:bank-reconciliation
│    Bank + Subledgers │  reconciliation-accounting:subledger-reconciliations
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. Preliminary TB    │  reconciliation-accounting:preliminary-trial-balance
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. Year-End Adjusts  │  year-end-accounting:year-end-adjustments
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 6. Adjusted TB       │  year-end-accounting:adjusted-trial-balance
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 7. MPERS Review      │  mpers-accounting:mpers-technical-review
│    Disclosures       │  mpers-accounting:disclosure-checklist
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 8. Financial Stmts   │  financial-statements-accounting:prepare-primary-statements
│    + Notes           │  financial-statements-accounting:prepare-notes
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 9. Quality Review    │  quality-review-accounting:quality-review
│                      │  quality-review-accounting:cross-tie-check
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 10. Finalisation     │  finalisation-accounting:finalise-accounts
│     Mgmt approval    │  finalisation-accounting:management-approval
│     Auditor / SSM    │  finalisation-accounting:auditor-pack | statutory-handoff
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 11. Tax (from lock)  │  tax-accounting:tax-computation
│                      │  tax-accounting:capital-allowances
└──────────────────────┘
```

## Gates (hard stops)

| After stage | Gate |
|---|---|
| Bank recon | Diff = RM0.00 |
| Preliminary TB | DR = CR |
| ATB | DR = CR |
| Primary FS | Assets = L + E |
| QC Section A | All pass |
| Finalisation | Management approval recorded |

## Domain builders (other jurisdictions)

To fork this marketplace for another domain/country:

1. Keep plugin **stage** names (bookkeeping → recon → YE → standards → FS → QC → finalise).
2. Replace `mpers-accounting` with your local GAAP plugin.
3. Replace `tax-accounting` references with local tax law files.
4. Swap COA templates and statutory deduction tables.
5. Keep `shared/guardrails.md` number-integrity rules — they are jurisdiction-agnostic.
