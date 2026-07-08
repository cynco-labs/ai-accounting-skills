# Agent Runtime Contract

How an AI agent should use this marketplace when a human **throws work at it** without naming a skill or slash command.

## Reality check

Humans will say things like:

- “Here’s the bank statements for ABC Sdn Bhd, do the year end”
- “Classify these transactions”
- “TB doesn’t balance, fix it”
- “Draft MPERS notes”

They will **not** say `/year-end-accounting:year-end-adjustments`.

So the default path is:

```
User dump (files + intent)
    → detect engagement context
    → load / update engagement state
    → route to the right stage skill (or full pipeline)
    → write artifacts
    → stop on blockers with a concrete ask
```

## Priority order for skill selection

When multiple skills could match, prefer in this order:

1. **`full-engagement-pipeline`** — if the user wants a full job, year-end, compilation, “do the accounts”, or dumps a folder of mixed source docs without a narrow ask
2. **The narrowest stage skill** that fully covers a *specific* ask (e.g. only bank recon)
3. **Never** invent a parallel ad-hoc workflow that skips gates

If firm profile is missing → run or offer `cold-start-interview` **once**, or continue in `[PROVISIONAL]` mode only if the user opts in.

## Engagement state (mandatory for multi-turn work)

Every multi-step engagement writes:

```
clients/<slug>/engagement_state.json
```

Schema: `references/engagement_state.schema.json`  
Rules:

- Read state **before** doing work
- Update `current_stage`, `status`, `artifacts`, `blockers`, `updated_at` after each stage
- Resume from `current_stage` — do not restart the pipeline silently
- If state says `blocked`, fix the blocker or ask the user; do not skip ahead

## Stage artifact contracts

See `references/stage_artifacts.md`. A stage is not “done” until its required artifacts exist and gates pass.

Agents should **check files on disk**, not rely on chat memory.

## Loading doctrine

1. Load only the **active stage’s** `SKILL.md`
2. Load `shared/guardrails.md` once per engagement (or when producing numbers)
3. Load jurisdiction refs **on demand** (MPERS when reviewing standards, tax when computing tax)
4. Do not load all 31 skills into context

## Question batching

- Batch classification / document asks (max ~4 options per question group)
- Prefer one structured “blockers & queries” update over drip questions
- Distinguish **staff** questions (technical) vs **client** questions (plain language)

## What “agent-native” forbids

- Fabricating numbers to “finish”
- Skipping bank recon / TB balance because the user is in a hurry (unless they explicitly accept a documented limitation)
- Claiming a stage is complete without artifacts
- Using slash-command names in client-facing language

## Success signal

The agent can be interrupted mid-engagement, a new session opened later, and from `engagement_state.json` + artifacts alone resume correctly.
