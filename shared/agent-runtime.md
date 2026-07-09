# Agent Runtime Contract

How an AI agent should use this marketplace when a human **throws work at it** without naming a skill or slash command.

## Kernel first

**Throw-work:** load **`shared/runtime-brief.md`** first (one screen).  
Open kernel / shelf / operator / guardrails **only when that step needs them**.

Six intents: **do-books · extract · classify · post · present · prove**.  
Before extract: **one intake** (shelf + register + state).  
Two axes: **`operator`** + **depth**. Done is **depth-scoped** (books-only ≠ year-end).  
TB only via `scripts/roll_tb.py` / `npx @cynco/accounting-skills tb`.

## Reality check

Humans will say things like:

- “Here’s the bank statements for ABC Sdn Bhd, do the year end”
- “Here are some receipts and banks in this folder, please do the accounting” ← **often zero company context**
- “Classify these transactions”
- “TB doesn’t balance, fix it”

They will **not** say `/year-end-accounting:year-end-adjustments`.

So the default path is:

```
User dump (cwd and/or scattered paths + intent)
    → runtime-brief
    → ONE intake (shelf + register + state + ≤3 asks)
    → books (extract → classify → post → recon → TB)
    → deeper stages only if engagement_type needs them
    → stop on true blockers; depth-scoped done
```

Client context is **our** problem. Detail: `shared/runtime-brief.md` · `shared/shelf-first.md` · `shared/smart-intake.md`.

## Install surface

Prefer the **umbrella** plugin `accounting-engagement` (one install, all stage skills).  
Modular plugins remain for partial installs. Sync: `scripts/sync_umbrella.py`.

## Priority order for skill selection

When multiple skills could match, prefer in this order:

1. **`resume-engagement`** — if `engagement_state.json` exists and the user is continuing / new session
2. **`full-engagement-pipeline`** — full job / folder dump / “do the accounts” (starts with **smart-intake** when context is thin)
3. **`smart-intake`** — explicit “I don’t know the company details, just this folder”
4. **`extract-bank-statement`** — bank PDF/CSV; Maybank Islamic → run `scripts/extract_maybank_islamic_pdf.py` (text+regex+balance proof, not vision-first)
5. **The narrowest stage skill** for a *specific* ask (e.g. only bank recon)
6. **Never** invent an ad-hoc workflow that skips gates or interrogates the user for facts already in the PDFs

If firm profile is missing → run or offer `cold-start-interview` **once**, or continue in `[PROVISIONAL]` mode only if the user opts in.

## Ledger system of record (Beancount + Fava)

Excel/openpyxl = working papers for humans.
**Beancount** (`.beancount`) = final double-entry system of record after books balance.
**Fava** = local web UI (`scripts/run_fava.sh ledger/main.beancount`).

After finalisation (or on request):

```bash
python3 scripts/export_to_beancount.py --client-dir <client> --output <client>/ledger/main.beancount --bean-check
scripts/run_fava.sh <client>/ledger/main.beancount
```

See `references/beancount_integration.md` and skills `export-beancount` / `open-fava`.

After writing workpapers, run:

```bash
python3 scripts/validate_engagement_artifacts.py <client_dir>
```

## Engagement state (mandatory for multi-turn work)

Every multi-step engagement writes:

```
clients/<slug>/engagement_state.json
```

Schema: `references/engagement_state.schema.json`  
Rules:

- Read state **before** doing work
- Ensure **`operator`** and **`engagement_type`** are set (resolve via `shared/operator-lens.md` if missing)
- Update `current_stage`, `status`, `artifacts`, `blockers`, `updated_at` after each stage
- Resume from `current_stage` — do not restart the pipeline silently
- If state says `blocked`, fix the blocker or ask the user; do not skip ahead
- Adapt **copy and deliverables** to `operator`; never change script math

## Stage artifact contracts

See `references/stage_artifacts.md`. A stage is not “done” until its required artifacts exist and gates pass.

Agents should **check files on disk**, not rely on chat memory.

## Loading doctrine

1. Load only the **active stage’s** `SKILL.md`
2. Load `shared/guardrails.md` once per engagement (or when producing numbers)
3. Load jurisdiction refs **on demand** (MPERS when reviewing standards, tax when computing tax)
4. Do not load all skills into context — one stage at a time

## Question batching + structured tools (mandatory)

Load **`shared/user-questions.md`**.

- **Period on disk is truth** — book that period deeply; do not force 12 months to start  
- Soft-confirm entity + period; use structured tool when available  
- Ask full-year / missing-month questions **only** if user already wants YE FS with gaps  
- Max **3** questions per call · **~5** options · recommended = work with what we have  
- `queries.md` = paper trail, not a substitute for the tool  
- Never treat silence as acceptance unless soft-confirm was already logged  
- Batch material classify; staff = codes, client = plain language

## Deliverable stack (no nonsense)

| Layer | Technology | Role |
|---|---|---|
| Intermediate truth | JSON under `workpapers/` | Machine-checkable |
| Human packs | **openpyxl** Excel (not Excel app at generate time) | Review / client |
| Ledger SoR | **Beancount** `.beancount` | Final double-entry |
| Interactive UI | **Fava** localhost | Explore balances |

See `shared/excel_deliverables.md` and `shared/architecture.md`.

## What “agent-native” forbids

- Fabricating numbers to “finish”
- Skipping bank recon / TB balance because the user is in a hurry (unless they explicitly accept a documented limitation)
- Claiming a stage is complete without artifacts
- Using slash-command names in client-facing language
- Treating Excel as the only place numbers live after finalisation

## Success signal

The agent can be interrupted mid-engagement, a new session opened later, and from `engagement_state.json` + artifacts alone resume correctly.
