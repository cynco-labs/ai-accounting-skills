---
name: smart-intake
description: >
 Document-first intake for folder dumps — infer context, ≤3 structured
 questions (do the books). Use when do the accounting without company
 details.
---

# /smart-intake

## Purpose

Make **folder-dump accounting** feel seamless.

The user is not responsible for knowing MPERS, FYE, or form codes. 
**We** read the folder, normalize context, and ask only smart questions.

## Load first

1. `shared/smart-intake.md` (mandatory doctrine) 
2. `shared/user-questions.md` (structured ask tool — mandatory for Tier B/C) 
3. `shared/guardrails.md` 
4. `shared/agent-runtime.md` 
5. Firm profile **if present** (defaults only — do not re-interview the firm)

## When to use

- User points at a folder / drops files and says do accounting / year end / books 
- Company name, country, or FY **not** stated 
- First contact for this client 

If `engagement_state.json` already exists → use `resume-engagement` instead.

## Workflow

### Step 0 — Scope the ask (silent default)

**Period truth first:** whatever bank months exist → that is the books period. Work it deeply.

| User vibe | Default engagement_type | Say once |
|---|---|---|
| “Do the accounting / sort my books” / folder dump | `bookkeeping_only` for **period on disk** | “I’ll fully book the months you gave (extract→TB→ledger). Full-year FS only if you want it and coverage is complete.” |
| Explicit “year end / prepare FS” + **complete** months | `year_end` | Proceed toward FS after books |
| Explicit “year end” + **partial** months | `bookkeeping_only` + AMBER | Finish available months; offer upgrade when more banks arrive — **do not stall** |
| “Tax only” | tax path later | — |
| “Just categorise” | bookkeeping_only | — |

Do not open with “Compilation or audit or review?” 
Do not recommend “bring 12 months before I start.”

### Step 1 — Inventory the folder (no questions)

List files with type guess:

- bank statement / export 
- receipt / invoice 
- payslip 
- SSM / registration 
- prior FS / tax 
- unknown 

Write draft `source/register.md`.

### Step 2 — Read high-signal docs first

Order:

1. Bank statements (PDF/CSV) — account title, bank brand, currency, date range, balances 
2. Invoices/receipts — supplier names, SST, amounts 
3. Any registration / prior FS if present 

Start `extract-bank-statement` / CSV normalize **in the same session** once banks are identified. Do not wait for the questionnaire.

### Step 3 — Build Hypothesis Card

Produce the card from `shared/smart-intake.md`. 
Fill `inferences[]` with field, value, confidence, evidence.

### Step 4 — Ask ≤ 3 questions — **structured tool required** (but don’t over-ask)

Rules:

- Never ask Tier A facts 
- Soft-confirm **entity + period-on-disk** (one question is enough for most dumps) 
- Max **3** questions · multiple-choice (3–5 options) 
- **MUST** use structured tool when asking (`shared/user-questions.md`) 
- Mirror into `workpapers/queries.md` — **not instead of** the tool 
- **Do not** ask “will you supply the other 7 months?” unless they already demanded full-year FS 
- Keep extracting/booking the months you have while soft-confirm is open 

Example (good):

```text
Q1 Soft-confirm? → Accept Acme · MYR · banks cover Mar–Nov 2025 (Recommended) | Fix entity | Fix period
```

Example (only if they asked for year-end FS with gaps):

```text
Q2 Coverage gap: Finish Mar–Nov books now (Recommended) | Pause until more months | Keep going; I’ll add months later
```

**Bad:** Recommended option = “Provide all 12 months before we continue.” 

**Do not** only paste a “Need you on:” bullet list in chat and continue.

### Step 5 — Write state & continue

Create workspace + `engagement_state.json`:

```json
{
 "schema_version": "0.0.1",
 "client_slug": "<from-name-or-folder>",
 "legal_name": "<best guess or UNKNOWN — CONFIRM>",
 "current_stage": "source_documents",
 "status": "waiting_on_user",
 "provisional": true,
 "notes": "Smart intake: inferences in README; provisional until identity confirmed"
}
```

Also write `README.md` section **## Inferences** and **## Open questions**.

Then **continue non-blocked work**:

- finish bank extraction for available months 
- classify high-confidence patterns 
- build gap list (missing months, no openings, etc.) 

### Step 6 — Gate for “final” work

| Work | Allowed on partial months? |
|---|---|
| Extract, classify, post, recon, TB, Beancount for **available** months | **Yes — default path** |
| Draft management P&L/BS labeled DRAFT / LIMITED PERIOD | Yes |
| Deep classify adjudication + payee map for that period | Yes |
| Final **signed full-year** FS | **No** — need complete coverage + identity + QC |
| Claiming “full year complete” with missing months | **No** |
| Refusing to book because months < 12 | **Forbidden** |

## Entity-type heuristics (Malaysia pack default when bank is MY)

| Evidence | Guess |
|---|---|
| “Sdn Bhd” / “Sdn. Bhd.” / “Sendirian Berhad” | Sdn Bhd → MPERS → Form C |
| “PLT” / “LLP” | PLT → MPERS → Form PT |
| “Bhd” without Sdn (careful) | possible Berhad → MFRS — confirm |
| Personal name account, Grab/food receipts, no co. suffix | sole prop candidate — confirm |
| “Enterprise” / “Ent” | often sole prop / enterprise — confirm |

If jurisdiction is **not** inferable (foreign bank only, USD account, no clues):

Ask **one** question: “Which country should these accounts be reported under?” 
Do not dump the whole entity matrix.

## Anti-patterns (do not do)

1. Firm cold-start interview when they only dropped client files 
2. Asking for framework/tax form before entity type 
3. Stopping all extraction until every field is filled 
4. Inventing company registration numbers or directors 
5. Ten classification questions one-by-one (batch by payee) 
6. **Prose-only Tier C asks** when a structured question tool exists 
7. Writing `queries.md` and treating that as “user was asked” without a tool call


## Completion

**Done when:** Hypothesis Card written, ≤3 asks issued if needed, extract started for banks on disk, engagement state provisional or confirmed.

## Outputs

- `source/register.md` 
- Hypothesis Card in chat 
- `README.md` inferences 
- `engagement_state.json` 
- Partial `workpapers/transactions.json` if banks readable 
- ≤3 questions 

## Next

- User answers → clear `provisional` flags as appropriate → `full-engagement-pipeline` 
- Or continue pipeline stages already unblocked 
