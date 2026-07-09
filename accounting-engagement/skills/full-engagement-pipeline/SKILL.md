---
name: full-engagement-pipeline
description: >
  Default for throw-work: dump a folder, "do the accounting", "sort my books",
  year end, prepare financial statements / MPERS pack without naming a stage.
  One intake then books; resumes from engagement_state.json. Depth-scoped done.
---
# Full engagement pipeline (agent-native entry)

## Purpose

Default when the human **does not** name a stage.  
**User short name:** `/do-books`. Natural language: “do the accounting.”

You are an engagement manager — not a slash menu.

1. Find docs (cwd, `@` paths, multi-folder)  
2. **One intake** — shelf + register + state + ≤3 asks  
3. Run **books** (extract → classify → post → recon → TB)  
4. Go **deeper** only if `engagement_type` needs it  
5. Stop cleanly on blockers; depth-scoped **Done when**

## Load first (keep light)

1. **`shared/runtime-brief.md`** — mandatory one-screen rules (read fully)  
2. Firm profile **if present** (quiet defaults — no firm interview on a personal dump)  
3. Active stage skill body only (one at a time)  

Open deeper docs **on demand** (table in runtime-brief). Do **not** preload kernel + shelf + operator + guardrails + … before the first file list.

## Intent router

| Signal | Route |
|---|---|
| Resume + `engagement_state.json` | Continue at progress; skip re-intake |
| Folder dump / “do accounting” | **This pipeline** (intake → books) |
| Only bank recon / classify / tax / revenue / capex | That narrow skill |
| “Set up the firm” only | `cold-start-interview` — **not** on client dumps |

**Folder-dump rule:** no blank questionnaire. Shelf → soft-confirm → extract same session.

## One intake (replaces separate shelf / setup / source ceremonies)

Do **once** at job start (or when new unsorted files arrive):

| Step | Action | Artifact |
|---|---|---|
| Discover | cwd + user paths only | working list |
| Job map | multi-entity → pick active | show table if >1 |
| Shelf | `clients/<slug>/source/**` | copy or pointer |
| Register | coverage matrix | `source/register.md` |
| State | operator + engagement_type + stage | `engagement_state.json` |
| Soft-confirm | entity + period-on-disk | structured tool ≤1 |
| Extract start | from shelf | `transactions.json` underway |

Detail if needed: `shared/shelf-first.md` · `shared/smart-intake.md` · `client-workspace`.  
**Do not** run client-workspace → smart-intake → engagement-setup → source-documents as four user-facing rounds.

Skills `source-documents` / `engagement-setup` only **verify** artifacts if something is missing.

## State

Path: `clients/<slug>/engagement_state.json`  
Schema: `references/engagement_state.schema.json`

### On start

```
IF engagement_state.json exists:
  load → ensure operator + engagement_type
  status board (six jobs) → resume work
ELSE:
  one intake (above) → books
```

### After each advance

1. Write artifacts · gate check  
2. Update state (`current_stage` may be fine-grained **internally**)  
3. Status board in **six jobs** for the human  
4. `updated_at` ISO-8601  

### Status board (user-facing)

```markdown
## [Legal name] · [period] · books only | year-end
| Step | Status | Notes |
|---|---|---|
| Organize | Done | Folder ready |
| Extract | Done | N bank lines |
| Classify | Needs you | structured options above |
| Post | Next | Journals + trial balance |
| Present | HTML pack | outputs/<slug>_pack.html |
| Prove | Later | depth_gates --strict |

**I need from you:** … (question tool — not a queries.md dump)
**Read:** open the HTML pack — not a stack of .md files
**Next from me:** …
```

Plain language for `operator: owner`. No internal stage keys for owners.

## Work sequence

### A — Books (default path — almost everyone)

| # | Work | How | Gate |
|---|---|---|---|
| 1 | Extract | `extract-bank-statement` / `npx … extract` | lines + balance proof |
| 2 | Classify | `classify-transactions` (+ substance if standards_aware) | codes or queries |
| 3 | Post | `post_journals.py` | JEs balance |
| 4 | Bank recon | bank-reconciliation | diff 0.00 or limitation |
| 5 | Prelim TB | `roll_tb.py --preliminary` only | DR=CR |
| 6 | HTML pack | `generate_html_report.py` | `outputs/*_pack.html` (required) |

**bookkeeping_only → STOP here** after HTML pack.  
Say: books ready · **open the HTML path**.  
Optional only: Beancount export · Fava (explore, not handoff).

### B — Deeper (only if engagement_type says so)

| When | Work |
|---|---|
| year_end / compilation / year_end_tax | YE journals → adjusted TB → standards review → primaries → notes → QC → finalise |
| year_end_tax | + tax from locked figures |
| User asked FS | upgrade type, then B |

Subledgers: only if material balances exist — not a ritual empty stage.

### C — Ledger (optional anytime books balance)

`export-beancount` → `open-fava` if user wants UI.

## Orchestration rules

1. Disk is truth  
2. Stop on true blockers (TB≠0, bank≠0 without limitation)  
3. Structured asks only for gates (`shared/user-questions.md`)  
4. Scripts for math — never type TB totals  
5. Partial runs OK (“stop after TB”)  
6. CLI is for the agent; narrate outcomes to the user  

## Depth & classify

| engagement_type | classify_depth | Present/prove |
|---|---|---|
| bookkeeping_only | bookkeeping (unless user wants proper classifications) | no FS pack required |
| year_end / compilation / year_end_tax | standards_aware | full pack |

## Done when (depth-scoped)

**Machine check (required before `status: done`):**

```bash
python3 scripts/depth_gates.py <client> --strict
# or close:
python3 scripts/close_engagement.py <client> --no-export-ledger
```

| Claimed depth | Required (see `references/depth_gates.json`) |
|---|---|
| **bookkeeping_only** | register · txns · journals · bank recon · prelim TB · **HTML pack** |
| **year_end** / **compilation** | books + YE · ATB · primaries · notes · QC Section A · HTML |
| **year_end_tax** | year-end + tax computation |
| User early stop | State + limitation note; do not claim full YE complete |

On books-only green: **open HTML pack** + “books ready” — do not chase FS/QC.  
**Forbidden:** forcing YE pack on a books-only dump.  
**Forbidden:** `status: done` when `depth_gates --strict` fails.  
**Forbidden:** handoff is a list of `.md` files.

## Failure modes

| Failure | Behavior |
|---|---|
| No entity name | Infer; soft-confirm; extract in parallel |
| Partial months | Book them fully; no stall for 12 months |
| Agent loads 10 doctrine files first | Use runtime-brief only |
| Agent re-runs full setup every turn | Resume from state |
| Agent pressures full year | Forbidden |

## Output language

- owner: plain; six-job board  
- bookkeeper: process + light codes  
- firm: technical OK on staff channel  
- Never dump slash walls at end users  
