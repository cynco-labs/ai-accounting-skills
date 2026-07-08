---
name: smart-intake
description: >
  Document-first client intake when the user dumps a folder of bank statements,
  receipts, or invoices with little or no company context. Infer jurisdiction,
  currency, entity name, period, and entity type from the files; confirm only
  what is ambiguous; ask at most 3 high-leverage questions. Trigger on: "do the
  accounting", "whatever is in this folder", "here are my banks and receipts",
  "please sort my books", messy client dump, no company name given, unknown
  entity, "I don't know the details just do it". Prefer this before a long
  engagement questionnaire. Does not fabricate registration numbers or balances.
---

# /smart-intake

## Purpose

Make **folder-dump accounting** feel seamless.

The user is not responsible for knowing MPERS, FYE, or form codes.  
**We** read the folder, normalize context, and ask only smart questions.

## Load first

1. `shared/smart-intake.md` (mandatory doctrine)  
2. `shared/guardrails.md`  
3. `shared/agent-runtime.md`  
4. Firm profile **if present** (defaults only — do not re-interview the firm)

## When to use

- User points at a folder / drops files and says do accounting / year end / books  
- Company name, country, or FY **not** stated  
- First contact for this client  

If `engagement_state.json` already exists → use `resume-engagement` instead.

## Workflow

### Step 0 — Scope the ask (silent default)

If user did not specify deliverable:

| User vibe | Default engagement_type | Say once |
|---|---|---|
| “Do the accounting / sort my books” | `year_end` with **limitations** if docs incomplete | “I’ll book what we have and flag gaps; full signed FS needs complete banks + your confirmation of the company name.” |
| “Tax only” | tax path later | — |
| “Just categorise” | bookkeeping_only | — |

Do not open with “Compilation or audit or review?”

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

### Step 4 — Ask ≤ 3 questions (Tier C only)

Rules:

- Never ask Tier A facts  
- Bundle Tier B into **one** soft-confirm sentence  
- Max **3** explicit questions this turn  
- Prefer multiple-choice when helpful  

Example first-turn ask:

> **Soft confirm:** Maybank + RM → Malaysia/MYR; account title **Acme Sdn. Bhd.**; statements **Mar–Nov 2025**.  
> **Need you on:**  
> 1. Is **Acme Sdn. Bhd.** the entity for these books (not personal)?  
> 2. Target year-end **31 Dec 2025** with Dec statement still missing — supply Dec or close a shorter period?  
> 3. Deliverable: full year-end pack vs bookkeeping + TB only for now?

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

| Work | Allowed while provisional? |
|---|---|
| Extract, classify, draft TB for available months | Yes |
| Draft management P&L/BS clearly labeled DRAFT / LIMITED | Yes |
| Final signed FS, tax filing advice under a name | **No** — need identity confirm |
| Claiming full-year complete with missing months | **No** |

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
