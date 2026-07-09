---
name: full-engagement-pipeline
description: >
  Default for throw-work: dump a folder, "do the accounting", "sort my books",
  year end, prepare financial statements / MPERS pack without naming a stage.
  Smart intake then one stage at a time; resumes from engagement_state.json.
---
# Full engagement pipeline (agent-native entry)

## Purpose

This is the skill the agent should load when the human **does not** specify a stage.  
**User short name:** `/do-books` (see `shared/slash-surface.md`).

You are not a menu of slash commands. You are an engagement manager that:

1. Detects what the user dropped 
2. Opens or resumes an engagement 
3. Runs stages in order 
4. Writes artifacts + state 
5. Stops cleanly on blockers with a concrete ask 

## Always load first

1. `shared/kernel-contract.md` — standard work files + scripts (first principles) 
2. `shared/skill-collapse-map.md` — six main jobs (do the books · extract · classify · post · present · prove) 
3. `CONTEXT.md` — plain English terms 
4. `shared/classify-substance.md` — classify = substance → analysis → code 
5. `shared/user-questions.md` — **progress asks must use structured question tools** 
6. `shared/agent-runtime.md` 
7. `shared/smart-intake.md` 
8. `shared/guardrails.md` 
9. `references/stage_artifacts.md` 
10. Firm profile if present (quiet defaults — **do not** firm-interview on a client dump) 

## Intent router (before stage 0)

| Signal | Route |
|---|---|
| Resume + `engagement_state.json` | `resume-engagement` → `current_stage` |
| Folder dump / “do accounting” / little client context | **`smart-intake` then this pipeline** |
| Full year-end with known entity | setup → pipeline |
| Only bank recon | `bank-reconciliation` |
| Only classify / “do the classifications” | `classify-transactions` (set `classify_depth`) |
| Revenue recognition only | `revenue-recognition` (thin → classify revenue theme) |
| Capitalise or expense only | `capitalise-or-expense` (thin → classify capex theme) |
| Only tax with P&L | `tax-computation` |
| “Set up the firm” / first install | `cold-start-interview` (firm, not client) |

**Folder-dump rule:** never open with a blank entity/framework questionnaire. 
Read files → Hypothesis Card → ≤3 questions → extract in parallel.

If ambiguous between full pipeline and one stage, default to full pipeline when banks/receipts for a period are present.

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
| 0a | smart_intake | smart-intake (if context thin / folder dump) | Hypothesis Card written; extraction started |
| 0 | setup | engagement-setup | Entity + FY + framework (may be provisional) |
| 1 | source_documents | source-documents | Bank coverage ok / override logged |
| 2a | record_transactions | extract-bank-statement (banks) then record-transactions | Lines extracted into transactions.json |
| 3 | classify_transactions | classify-transactions | Codes assigned or queried; **standards_aware** when year_end/compilation — analysis packs for material themes |
| 4 | journal_entries | journal-entries → **`post_journals.py`** | JE balance (engine) |
| 5 | bank_reconciliation | bank-reconciliation | Diff 0.00 |
| 6 | subledger_reconciliations | subledger-reconciliations | Material ties |
| 7 | preliminary_trial_balance | **`roll_tb.py --preliminary` only** (not freestyle) | DR=CR |
| 8 | year_end_adjustments | year-end-adjustments → `journals_ye.json` | Catalogue done; each YE JE balances |
| 9 | adjusted_trial_balance | **`roll_tb.py --adjusted` only** (not freestyle) | DR=CR; **source for FS** |
| 10 | standards_review | mpers-technical-review | Issues listed |
| 11 | primary_statements | prepare-primary-statements | BS balances |
| 12 | notes | prepare-notes | Ties to primaries |
| 13 | quality_review | quality-review | Section A pass |
| 14 | finalisation | finalise-accounts (+ management-approval) | Lock / approval |
| 14b | beancount_sor | export-beancount (+ validate-beancount) | bean-check PASS; `ledger/main.beancount` |
| 15 | tax | tax-computation | Optional; ties to lock |
| 16 | fava_ui | open-fava (optional, user-facing) | Fava URL shown |

### How to “load skill”

1. Read that skill’s `SKILL.md` from its plugin path 
2. Execute it fully until its **completion criterion** (or blocker) 
3. If plugin missing, use this file’s stage table + repo `references/` and still write the same artifacts 

Do **not** paste all skills into context. One stage at a time — defence against **premature completion** (see `shared/skill-craft.md`).

## Orchestration rules

1. **Disk is truth** — chat memory is not an artifact 
2. **Stop on blockers** — bank ≠ 0, TB ≠ 0, missing mandatory banks 
3. **Batch questions via structured tool** — `shared/user-questions.md`; never prose-only Tier C 
4. **No fabricated numbers** — re-read sources if context was compacted 
5. **Scripts for math** — extract / classify / post / roll_tb / close; never type TB totals 
6. **Provisional mode** — only if firm profile missing and user accepts `[PROVISIONAL]` tags 
7. **Partial runs** — user may say “stop after TB”; set state and exit cleanly 
8. **Interruptible** — any session can resume from state alone 
9. **waiting_on_user** — only after a structured ask (or ACTION REQUIRED fallback) was issued

### Kernel commands (prefer over chat freestyle)

```bash
npx @cynco/accounting-skills extract <source> --json workpapers/transactions.json
npx @cynco/accounting-skills classify workpapers/transactions.json
npx @cynco/accounting-skills post <client> --opening-from-bank
npx @cynco/accounting-skills tb <client> --both
npx @cynco/accounting-skills close <client>
npx @cynco/accounting-skills ledger <client>
```

## Scope flags

**Work the months you have** (see smart-intake + `shared/user-questions.md`):

1. Compute **coverage matrix** from bank files (truth of period). 
2. Default `engagement_type`: `bookkeeping_only` for that period — run the books **fully** for those months. 
3. Soft-confirm entity + period-on-disk. 
4. Upgrade to `year_end` / FS only when user wants it **and** coverage supports it (or they add months later). 

### Classify depth

| Engagement | `classify_depth` |
|---|---|
| `bookkeeping_only` (default dump) | `bookkeeping` unless user asks for proper classifications / revenue / capex |
| `year_end` / `compilation` / `year_end_tax` | **`standards_aware`** — substance packs before post |
| User: “do the classifications properly” | **`standards_aware`** |

Doctrine: `shared/classify-substance.md`. Analysis lives in `workpapers/analysis/`.

Do **not** ask framework/tax form/industry first. 
Do **not** treat incomplete calendar year as a reason to stop booking.


## Completion

**Done when:** target stages for this run complete (or clean stop with state + blockers); never claim final without prove gates.

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
| User dumps files, no entity name | **smart-intake**: infer; soft-confirm entity+period; extract in parallel |
| Partial bank months | **Book those months fully**; AMBER on full-year FS only — never stall for 12 months |
| User wants YE FS but months missing | Finish available period; offer upgrade when more files arrive |
| Agent pressures “must supply full year” | Forbidden |
| Agent tempted to skip recon | Forbidden unless user override logged in state.notes |
| Context loss mid-job | Re-read state + artifacts; never reconstruct numbers from memory |
