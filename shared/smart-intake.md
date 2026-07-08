# Smart intake — document-first, question-last

## The real user

They are **not** your problem to educate with a 20-field form.

They say:

> “Here are some bank statements and receipts in this folder. Please do the accounting.”

They may not know (or care to type):

- legal entity name  
- country / framework  
- financial year end  
- “MPERS vs MFRS”  
- what a trial balance is  

**That context is our problem.** The agent’s job is to **read the folder first**, form hypotheses, and only ask what cannot be inferred or verified.

## Seamlessness scorecard (design target)

| Dimension | Target |
|---|---|
| Time-to-first-useful-work | Extract banks/receipts **before** any long interview |
| Questions in first turn | **0–3**, never a blank questionnaire |
| Questions that restate the docs | **Zero** (if Maybank → do not ask “which bank?”) |
| Blocking asks | Only true blockers (identity of books owner if ambiguous; missing months if full-year promised) |
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

Ask only if still unknown **after** reading available files:

1. **Who is the reporting entity?** — only if multiple names appear (personal + company) or account title is blank/ambiguous  
2. **What should we produce?** — only if unclear: full year-end FS vs “just sort the books” vs tax only  
   - Default if silent: **management accounts / compilation path from available docs**, with limitations logged  
3. **Opening balances / prior year** — only if user wants comparative FS or equity continuity and no prior FS is in the folder  
4. **Missing bank months** — if they asked for “full year” but only 3 months exist: show coverage matrix, ask to supply rest **or** accept limited period  

**Do not ask** in the first batch:

- MPERS section-by-section  
- Depreciation rates (infer policy later or use firm defaults)  
- Full director list (unless related-party material and docs suggest directors)  
- Chart of accounts design  
- Tax form letter if entity type still open — derive after entity  

## First-turn protocol (mandatory for folder dumps)

```
1. List files (names, types, dates if in filename)
2. Open banks first (highest signal), then receipts/invoices
3. Build Hypothesis Card (below)
4. Start extraction into transactions.json for what exists
5. Ask at most 3 Tier-C questions, batched
6. Write engagement_state with inferences + open questions
7. Continue pipeline on non-blocked work while waiting
   (e.g. extract & classify clear items; park ambiguous payees)
```

**Never** block the entire job on a non-blocking unknown (e.g. industry label).

## Hypothesis Card (show the user)

```markdown
## What I can already see
| Field | Best guess | Confidence | Evidence |
|---|---|---|---|
| Legal name | Acme Sdn. Bhd. | high | Maybank account title |
| Country / pack | Malaysia | high | Maybank + RM |
| Currency | MYR | high | Statement |
| Period covered | 2025-03 → 2025-11 | medium | Statement dates (not full year) |
| Entity type | Sdn Bhd | high | “Sdn Bhd” in account title |
| Framework | MPERS | medium | Private company default (MY) |
| Output wanted | Year-end pack | low | You said “do the accounting” — confirm |

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
| When | First install of plugin | Every new folder dump |
| About | Your firm defaults | This client’s books |
| Skip if | firm-profile exists | inferences cover Tier A/B |

Do not run a full firm interview when the user only dropped a client folder. Use firm defaults quietly; client intake is separate.

## Failure modes to avoid

1. **Interrogation theatre** — asking what the PDF already says  
2. **False precision** — inventing company registration numbers  
3. **Stall** — refusing to extract until every field is filled  
4. **Silent wrong entity** — two names in folder; picked one without confirming  
5. **Scope creep questions** — full MPERS checklist before one bank is booked  
