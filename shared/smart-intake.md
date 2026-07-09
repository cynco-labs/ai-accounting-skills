# Smart intake — document-first, question-last

## The real user

They are **not** your problem to educate with a 20-field form.

They say:

> “Here are some bank statements and receipts in this folder. Please do the accounting.”

Or they `cd` somewhere messy, or `@`-mention paths on Desktop/Downloads. Docs may be **everywhere**.

They may not know (or care to type):

- legal entity name  
- country / framework  
- financial year end  
- “MPERS vs MFRS”  
- what a trial balance is  

**That context is our problem.** Order of work:

1. **Shelf the papers** (`shared/shelf-first.md`) — discover → cluster by entity/period → standard folders → register  
2. **Read** shelved sources → hypotheses  
3. **Ask** only what cannot be inferred  
4. **Extract** only from the shelf  

Never book from a random Desktop pile with no client folder.

## Seamlessness scorecard (design target)

| Dimension | Target |
|---|---|
| Time-to-first-useful-work | **Shelf + register** first; then extract banks **before** any long interview |
| Messy / multi-path inputs | Accept cwd + user paths; **never** require perfect folders up front |
| Multi-company dumps | Job map → one shelf per entity; don’t mix |
| Questions in first turn | **0–3**, never a blank questionnaire |
| Questions that restate the docs | **Zero** (if Maybank → do not ask “which bank?”) |
| Blocking asks | Only true blockers (ambiguous entity identity). Partial months are **not** a stop. |
| Period truth | Coverage = months on disk. Soft-confirm that. Do **not** demand 12 months to start. |
| Assumptions | Written to `engagement_state.json` / README with confidence |

## Infer → Confirm → Ask

### Tier A — Infer silently (high confidence)

Use without asking when evidence is strong:

| Signal in docs | Inference |
|---|---|
| Maybank / CIMB / Public Bank / RHB / Hong Leong / Bank Islam / AmBank | Jurisdiction pack `malaysia`, currency `MYR` (unless statement shows other) |
| Statement header currency MYR / RM | Currency MYR |
| Account title “X SDN BHD” / “X Sdn. Bhd.” | Entity type Sdn Bhd; legal name candidate = X |
| Account title personal name only, small activity | Possible sole prop — **medium**, confirm once |
| Statement date span e.g. Jan–Dec 2025 | Period candidate; FYE often 31 Dec if full calendar year present |
| Recurring “AEON”, “GRAB”, “SHOPEE”, “LAZADA” | Industry hint retail/consumer — overlay later |
| Landlord / “RENT” monthly | Rental expense pattern |
| “KWSP/EPF”, “PERKESO”, “LHDN” | Malaysian payroll/tax present |
| Folder name `abc-sdn-bhd-2025` | Slug + year candidate |
| Receipt language / SST invoice | Malaysia tax context |

Record as:

```yaml
inferences:
  - field: jurisdiction_pack
    value: malaysia
    confidence: high
    evidence: "Maybank e-statement header"
```

### Tier B — Soft confirm (one short line)

Show your working; user can correct with “yes” or a fix:

> “From the Maybank statements I’m treating this as **Malaysia / MYR**, account name **ACME SDN BHD**, period **Jan–Dec 2025**. OK unless you say otherwise.”

Do **not** ask five separate questions for those four facts.

### Tier C — Must ask (cannot invent)

Ask only if still unknown **after** reading available files.

**Mandatory delivery:** use the host **structured user-question tool** per `shared/user-questions.md`.  
Do **not** only list questions in chat or `queries.md`.

1. **Who is the reporting entity?** — only if multiple names appear (personal + company) or account title is blank/ambiguous  
2. **Period on disk (truth)** — always compute coverage (e.g. Jan–May 2026). Soft-confirm that period.  
   - Default work: **deep books for that period** (not “wait for 12 months”).  
3. **What to produce** — only if user explicitly wants year-end FS / tax and coverage is incomplete:  
   - Recommended: finish limited-period books now  
   - Optional: they will add months later  
   - **Never** make “supply all months first” the recommended path  
4. **Opening balances / prior year** — only if they need equity continuity / comparative FS and no prior FS is in the folder  

**Default if silent:** bookkeeping for **available months** → TB + recon + ledger, labeled limited period.  
Full-year MPERS pack is an **upgrade**, not the default for a partial dump.

**Tier B soft-confirm** via tool when provisional: one “Accept entity + period-on-disk / Fix …” question.

**Do not ask** in the first batch:

- MPERS section-by-section  
- Depreciation rates (infer policy later or use firm defaults)  
- Full director list (unless related-party material and docs suggest directors)  
- Chart of accounts design  
- Tax form letter if entity type still open — derive after entity  

## Operator + depth (same engine for everyone)

Load **`shared/operator-lens.md`**. Write both fields on `engagement_state.json` during intake:

| Field | What it is | Default on thin folder dump |
|---|---|---|
| **`operator`** | Who is driving: `owner` · `bookkeeper` · `firm` | Infer; else one soft-ask |
| **`engagement_type`** | How deep: books → year-end → tax | `bookkeeping_only` for period on disk |

**Infer operator without asking when strong:**

| Signal | `operator` |
|---|---|
| “my books / my company / my business” · personal-name account · no firm profile | `owner` |
| “I’m the bookkeeper for …” | `bookkeeper` |
| Real firm profile (not PLACEHOLDER) + “the client” / multi-client language | `firm` |
| Firm profile **Default operator:** set | use that |

Do **not** open with a firm cold-start when the dump looks personal. Do **not** invent separate business vs firm slash commands.

## First-turn protocol (mandatory for folder dumps)

```
1. DISCOVER — cwd + user-mentioned paths (shared/shelf-first.md); do not scan whole home
2. CLUSTER — entity + period job map; if multi-company, soft-confirm active job
3. SHELF — clients/<slug>/ layout; copy or pointer sources into source/<kind>/
4. REGISTER — source/register.md + coverage matrix
5. Peek banks first (headers), then receipts/invoices
6. Build Hypothesis Card (below) — include operator + depth guess
7. Resolve operator (infer → firm-profile default → one ask if needed)
8. Start extraction **from the shelf** into workpapers/transactions.json
9. Ask at most 3 Tier-C questions via **structured user-question tool** (see `shared/user-questions.md`), batched
10. Write engagement_state with operator, engagement_type, inferences + open questions
11. Continue pipeline on non-blocked work while waiting
```

**Never** block the entire job on a non-blocking unknown (e.g. industry label).  
**Never** refuse to book available months because a full financial year is incomplete.

## Hypothesis Card (show the user)

```markdown
## What I can already see
| Field | Best guess | Confidence | Evidence |
|---|---|---|---|
| Operator | owner | medium | “my books” + no firm profile |
| Legal name | Acme Sdn. Bhd. | high | Maybank account title |
| Country / pack | Malaysia | high | Maybank + RM |
| Currency | MYR | high | Statement |
| Period covered | 2025-03 → 2025-11 | medium | Statement dates (not full year) |
| Entity type | Sdn Bhd | high | “Sdn Bhd” in account title |
| Framework | MPERS | medium | Private company default (MY) |
| Depth | bookkeeping_only | medium | Folder dump default |

## What I’m doing next (no need to answer)
- Extract bank lines → classify obvious patterns
- Build source register + gap list for missing months

## I only need from you
1. …
2. …   (max 3)
```

## Question style

| Bad | Good |
|---|---|
| “Please provide entity type, framework, FYE, directors, COA, tax form, industry…” | “Account title says Acme Sdn Bhd — is that the company we’re reporting for?” |
| “What is the financial year?” | “Statements run Mar–Nov 2025. Is FYE 31 Dec 2025 with missing Dec still to come, or is the year only these months?” |
| “Which jurisdiction?” | *(don’t ask if Maybank/RM)* |
| “How should I classify every line?” | Group: “12 payments to TELEKOM — utilities?” |

## Parallel work while waiting

Allowed without user answer:

- Source register  
- Bank extraction  
- Auto-classify high-confidence patterns  
- Bank recon **for months present**  
- Query list for ambiguous payees  

Not allowed without identity clarity:

- Issuing “final signed FS” under a guessed legal name  
- Tax filing recommendations under wrong person/company  

## Firm cold-start vs client intake

| | Firm cold-start | Client smart intake |
|---|---|---|
| When | First install **and** operator will be `firm` (or user asks) | Every new folder dump |
| About | Practice defaults + **Default operator** | This entity’s books + **operator** + depth |
| Skip if | firm-profile exists | inferences cover Tier A/B |

Do not run a full firm interview when the user only dropped a personal/client folder. Use firm defaults quietly when present; intake still sets **this job’s** `operator`.

## Failure modes to avoid

1. **Interrogation theatre** — asking what the PDF already says  
2. **False precision** — inventing company registration numbers  
3. **Stall** — refusing to extract until every field is filled  
4. **Silent wrong entity** — two names in folder; picked one without confirming  
5. **Scope creep questions** — full MPERS checklist before one bank is booked  
6. **Skip the shelf** — extract/classify from Desktop with no `clients/<slug>/`  
7. **Mix companies** — one transactions.json for two legal names  
8. **Home-drive crawl** — scanning directories the user never named 
