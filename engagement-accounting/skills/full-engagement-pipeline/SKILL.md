---
name: full-engagement-pipeline
description: >
  DEFAULT entry when a user throws accounting work at the agent without naming
  a skill. Orchestrates Malaysian (and pack-based) engagements end-to-end:
  source documents, bookkeeping, bank recon, trial balance, year-end
  adjustments, MPERS/standards review, financial statements, notes, QC,
  finalisation, and tax. Trigger on: year end, year-end, YE accounts,
  compilation, "do the accounts", "prepare financial statements", "from bank
  statements", client folder dump, management accounts, full bookkeeping to FS,
  "process this client", "finish the books", mixed PDFs of banks/invoices/payslips
  for a period. Also use when the user resumes an in-progress engagement.
  Reads/writes clients/<slug>/engagement_state.json. Stops on blockers
  (unbalanced TB, bank not reconciling, missing statements). Prefer this over
  inventing an ad-hoc workflow. For a single narrow task only (e.g. only bank
  recon), use that stage skill instead.
---

# Full engagement pipeline (agent-native entry)

## Purpose

This is the skill the agent should load when the human **does not** specify a stage.

You are not a menu of slash commands. You are an engagement manager that:

1. Detects what the user dropped  
2. Opens or resumes an engagement  
3. Runs stages in order  
4. Writes artifacts + state  
5. Stops cleanly on blockers with a concrete ask  

## Always load first

1. `shared/agent-runtime.md`  
2. `shared/guardrails.md`  
3. `references/stage_artifacts.md`  
4. Firm profile if present: `~/.claude/plugins/config/claude-for-accounting/firm-profile.md`  

## Intent router (before stage 0)

Classify the user message + files:

| Signal | Route |
|---|---|
| Full year-end / compilation / “do the accounts” / client folder | **This pipeline** from setup or resume |
| Only bank statements + “reconcile” | `bank-reconciliation` (still create/update state) |
| Only “classify these” | `classify-transactions` |
| Only “tax computation” with final P&L | `tax-computation` |
| “Set up the firm” / first install | `cold-start-interview` |
| Resume + `engagement_state.json` exists | Jump to `current_stage` |

If ambiguous between full pipeline and one stage, **ask one clarifying question**, defaulting to full pipeline when a full period of banks is present.

## Engagement state machine

Path: `clients/<slug>/engagement_state.json`  
Schema: `references/engagement_state.schema.json`  
Example: `references/engagement_state.example.json`

### On start

```
IF engagement_state.json exists:
  load it
  show one-line status: client | FY | current_stage | status | open blockers
  IF status == blocked: focus on blockers first
  ELSE resume at current_stage
ELSE:
  create workspace (client-workspace conventions)
  write initial state (current_stage=setup, status=in_progress)
```

### After every stage

1. Write required artifacts (see stage_artifacts.md)  
2. Run gate checks  
3. Update state:
   - append stage to `stages_completed` if gate passed  
   - set `current_stage` to next  
   - set `status` to `in_progress` | `blocked` | `waiting_on_user` | `waiting_on_client`  
   - write `artifacts` map  
   - set `updated_at` ISO-8601  
4. Emit a short **status board** to the user  

### Status board format (every turn that advances work)

```markdown
## Engagement status — [Legal name] FYE [date]
| Stage | Status | Artifact |
|---|---|---|
| source_documents | ✅ | source/register.md |
| record_transactions | ✅ | workpapers/transactions.json |
| classify_transactions | 🟡 waiting_on_user | 6 payees need codes |
| … | ⬜ | |

**Blockers:** …
**Next action:** …
```

## Pipeline stages (mandatory order)

| # | Stage key | Load skill | Gate |
|---|---|---|---|
| 0 | setup | engagement-setup | Entity + FY + framework |
| 1 | source_documents | source-documents | Bank coverage ok / override logged |
| 2 | record_transactions | record-transactions | Lines extracted |
| 3 | classify_transactions | classify-transactions | Codes assigned or queried |
| 4 | journal_entries | journal-entries | JE balance |
| 5 | bank_reconciliation | bank-reconciliation | Diff 0.00 |
| 6 | subledger_reconciliations | subledger-reconciliations | Material ties |
| 7 | preliminary_trial_balance | preliminary-trial-balance | DR=CR |
| 8 | year_end_adjustments | year-end-adjustments | Catalogue done |
| 9 | adjusted_trial_balance | adjusted-trial-balance | DR=CR |
| 10 | standards_review | mpers-technical-review | Issues listed |
| 11 | primary_statements | prepare-primary-statements | BS balances |
| 12 | notes | prepare-notes | Ties to primaries |
| 13 | quality_review | quality-review | Section A pass |
| 14 | finalisation | finalise-accounts (+ management-approval) | Lock / approval |
| 15 | tax | tax-computation | Optional; ties to lock |

### How to “load skill”

1. Read that skill’s `SKILL.md` from its plugin path  
2. Execute it fully for this stage  
3. If plugin missing, use this file’s stage table + repo `references/` and still write the same artifacts  

Do **not** paste all skills into context. One stage at a time.

## Orchestration rules

1. **Disk is truth** — chat memory is not an artifact  
2. **Stop on blockers** — bank ≠ 0, TB ≠ 0, missing mandatory banks  
3. **Batch questions** — classification groups; one board of client queries  
4. **No fabricated numbers** — re-read sources if context was compacted  
5. **Provisional mode** — only if firm profile missing and user accepts `[PROVISIONAL]` tags  
6. **Partial runs** — user may say “stop after TB”; set state and exit cleanly  
7. **Interruptible** — any session can resume from state alone  

## Scope flags (ask once if unknown)

- Engagement type: bookkeeping_only | compilation | year_end | year_end_tax | audit_support  
- Framework / jurisdiction pack  
- Industry overlay (trading, services, fnb, property, construction, none)  
- Skip tax? Skip full notes (management accounts only)?  

Store answers in `engagement_state.json`.

## Output to human (language)

- Staff: account codes, DR/CR, gates  
- Client-facing lists: plain language, numbered, actionable  
- Do not dump slash-command names at clients  

## Done criteria

`current_stage == complete` and `status == done` only when:

- QC Section A passed  
- FS pack exists  
- Finalisation recorded (or user explicitly stopped earlier with documented limitation)  
- Tax done if `engagement_type` includes tax  

## Failure modes

| Failure | Behavior |
|---|---|
| User dumps files, no entity name | Infer from docs; else ask once |
| Missing months of bank | Block or AMBER limitation in state |
| Agent tempted to skip recon | Forbidden unless user override logged in state.notes |
| Context loss mid-job | Re-read state + artifacts; never reconstruct numbers from memory |
