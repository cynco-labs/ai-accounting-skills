# User questions — structured tools required

**Problem this solves:** agents dump Tier-C asks into chat or `queries.md`, users never click through, work stalls or agents invent answers.

**Rule:** any question that **gates progress**, **needs a real choice**, or **would otherwise become an “open query” the user must solve alone** must use the host’s **structured user-question tool** when available — not prose alone.

## First principles

1. **You are the guide, not the homework assigner.**  
   Never end a run with “here are 7 open queries — please confirm.”  
   End with **explained choices** that resolve the books when the user picks one.

2. **Every open query has three parts** before it becomes a tool ask:
   - **What we saw** (facts + £/RM amounts from source — never invented)
   - **What we already booked** (so the user knows the default)
   - **What the choice will change** (debtor / expense / suspense / leave as cash)

3. **`queries.md` is a paper trail.**  
   It records the same asks + answers after the tool. It is **not** the user interface.

4. **Batch by theme, not by document number.**  
   One question for “all customer short-receipts,” not four separate invoice quizzes.

5. **Recommended option = safe default for this depth.**  
   For bookkeeping_only, preferred default is usually: *keep cash as truth, leave variance off books until docs arrive* — label it Recommended when that is true.

---

## Work the months you have, not year-first (product truth)

Agents must **not** pressure users into a 12‑month year-end when the dump is partial.

| Principle | Behavior |
|---|---|
| **Truth of period** | Coverage = months **on disk**. Write it. Soft-confirm it. |
| **Default work** | Do **full bookkeeping depth** on that period (extract → classify → post → recon → TB → ledger). |
| **Full-year FS** | Only if user **opts in** *and* bank coverage is complete (or they supply the rest). |
| **Never** | Recommend “you must get 12 months” or make the user “promise Dec” to continue. |
| **Never** | Stall extract/classify/TB waiting for missing months the user did not ask for. |

Missing months are an **with limitation** note on full-year claims — not a red stop on bookkeeping for what exists.

---

## When the tool is mandatory

Use the structured question tool **before** setting `status: waiting_on_user` for these:

| Situation | Examples |
|---|---|
| **Soft confirm (identity + period truth)** | “Treat as Acme · MYR · **period on disk Jan–May 2026**?” |
| **Entity identity** | Only if multiple names / personal vs company unclear |
| **Classification adjudication (material)** | Payee batch with 3–5 account options |
| **Invoice / bill vs bank variance** | Customer short/over receipt; supplier over/under pay vs bill PDF |
| **Opening / prior year** | Provisional plug vs wait — only if openings block *their* goal |
| **Payroll / tax completeness gaps** | Employer NIC missing; pension not on summary |
| **User asked for full year-end but months missing** | Then ask: work limited period now vs wait for more months — **not** “you must supply 12 months” |
| **Blocker resolution** | User override of a hard gate (must be explicit) |
| **Finalisation / approval** | Management approval recorded |

**Do not** open with a deliverable quiz that implies full year is the only serious path.

### Variance resolution is mandatory (not a dump)

After extract + classify, if any material line has **document amount ≠ bank amount**, you **must**:

1. Book a **safe interim** (cash = bank; no invented AR/AP).
2. Write the variance table to `workpapers/queries.md` (trail).
3. **Immediately** call the structured question tool (≤3 themes) so the user can resolve.
4. On answer → re-post journals / roll TB / refresh HTML pack.
5. Only then mark books `done` for that theme (or log explicit “leave cash-only” choice).

**Forbidden:** list variances under “Open queries” and set `status: done` without a structured ask (unless the user already answered the same theme earlier this engagement).

## When prose / `queries.md` alone is OK

| Situation | Why |
|---|---|
| Status board only (no ask) | Informational |
| Long client query pack **after** structured asks already captured | Paper trail |
| Host has **no** question tool (see fallback) | Documented exception |
| Non-blocking FYI for staff later (immaterial, no book impact) | Not a gate |

**Never:** only append to `workpapers/queries.md` and continue as if the user answered.  
**Never:** present “open queries” as the main user deliverable.

---

## Host tool map

Pick the **first available** tool in the session. Do not invent tool names.

| Host / agent | Structured tool (typical) | Notes |
|---|---|---|
| **Grok / xAI Build** | `ask_user_question` | Prefer; supports multi-select |
| **Claude Code / Cowork** | `AskUserQuestion` (or host equivalent) | Use if present in tool list |
| **Cursor / Codex / others** | Host “ask user” / form tool if listed | Probe tools at runtime |
| **No tool** | Fallback protocol below | Still force answerable format |

At skill load time: if a structured question tool appears in your available tools, **you must call it** for mandatory cases. Skipping it is a skill failure.

---

## Shape of a good structured ask

### Soft confirm (1 question, single-select) — preferred first ask

State the **actual period on disk**, not a hoped-for FY.

```text
Question: Does this look right to book?
Options:
  - Yes — [Legal name] · [MYR] · banks cover [Jan–May 2026] · [bank]  (Recommended)
  - Wrong company name — I’ll correct it
  - Wrong months — I’ll narrow or fix the period
```

No “must supply full year” option. Depth of work is implied: we book **this period**.

### Operator (only if not inferable) — single-select

See `shared/operator-lens.md`. Prefer inferring; ask at most once per install/job.

```text
Question: Who are these books for?
Options:
  - My own business (Recommended when the folder looks personal)
  - I’m the bookkeeper for this company
  - A client of our accounting firm
```

Write answer to `engagement_state.operator` (`owner` | `bookkeeper` | `firm`).

### Upgrade to full year-end (only if user already asked for YE / FS)

```text
Question: Bank files only cover [Jan–May]. What should we do?
Options:
  - Finish full books for Jan–May now (Recommended) — trial balance, bank recon, optional ledger
  - Pause — I’ll add more months first
  - Keep going on Jan–May; I’ll add months later for a full-year pack
```

**Wrong option (never use as recommended):** “You must provide all 12 months before we start.”

### Classification batch (1–3 questions, multi-select only if host supports)

```text
Question: Where should we put ~RM 364k in (3 similar receipts)?
Options:
  - Sales — Food & beverage (code 4000) (Recommended if customer/card settlement)
  - Not sales — bank float or clearing
  - Loan or financing money in
  - Hold in suspense — need more documents
```

### Variance batch — sales short/over receipts (template)

Explain in the **question text** (one short paragraph), then options that **change the books**:

```text
Question: Three customer invoices total more than the bank received
(£4,021 short across INV-1040/41/42). We booked sales at the bank amount only.
How should we treat the gaps?
Options:
  - Keep cash only for now — leave gaps off the books (Recommended for books-only)
  - Book the shortfalls as money still owed by customers (trade debtors)
  - Treat as credit notes / write-offs against sales
  - Hold gaps in suspense until you send statements or credit notes
```

### Variance batch — purchase bill ≠ bank payment (template)

```text
Question: Five supplier bills don’t match what left the bank
(some over-paid vs bill, some under). We booked expenses at the bank amount.
What should we do?
Options:
  - Keep bank amount as expense — ignore bill PDFs for totals (Recommended if bills look wrong)
  - Rebook to match each bill; difference becomes creditor or prepaid
  - Split: match where close, suspense the rest
  - Hold all five in suspense — you’ll send corrected invoices
```

### Completeness gap — payroll (template)

```text
Question: March payroll shows employee deductions but no employer NIC.
We booked gross salaries + employee PAYE/NIC/pension only.
Options:
  - Leave as is — employer NIC not in this pack (Recommended if amount unknown)
  - I’ll type the employer NIC figure next (then we accrue)
  - Use HMRC Month 11 employer NIC as a rough proxy (only if you confirm)
```

**Limits:**

- Max **3 questions** per tool call (matches smart-intake).
- Max **~5 options** per question.
- First option = **recommended** when you have a best guess; label it “(Recommended)”.
- Options must be **actions that resolve the ledger**, not “please investigate offline.”
- Staff = codes OK in option labels; owner = plain language only.
- Put £/RM **in the question**, not only in a markdown appendix.

---

## Workflow (mandatory order)

```text
1. Inventory + infer period coverage from files (truth matrix)
2. Soft-confirm via tool: entity + period-on-disk (≤1 ask if needed)
3. Extract / classify / post / TB for months present — do not wait
4. Detect variances + completeness gaps → structured tool (≤3 themes)
5. Persist answers → re-post / roll TB / refresh human pack (HTML)
6. Write queries.md as trail of asks + answers (not the UI)
7. Full-year / FS / tax only when coverage + user intent support it
```

**While waiting on soft-confirm:** keep running extract/classify/post/tb for available months.  
**While waiting on variance answers:** keep interim cash books + HTML pack; status `waiting_on_user` for those themes only.  
**Do not** invent entity name or claim full-year complete without evidence.

---

## Fallback (no question tool)

If and only if no structured tool exists:

1. Emit a single markdown block titled **`## ACTION REQUIRED — reply with option letters`**
2. Number questions 1–3; each option **A/B/C/D**
3. Set `engagement_state.status = waiting_on_user`
4. **Do not** continue stages that need those answers
5. On next user message, parse letter answers first; if ambiguous, ask again with the tool or the same block

Example:

```markdown
## ACTION REQUIRED — reply with option letters

**1. Soft-confirm context?**
- **A (Recommended)** — CJT Bakery Sdn. Bhd. · MYR · Jan–May 2026 · Maybank ****4296
- **B** — Fix entity name (reply with name)
- **C** — Fix period

**2. Deliverable?**
- **A (Recommended)** — Limited-period books + TB only
- **B** — Full year-end (I will add missing months)

Reply e.g. `1A 2A`
```

---

## Persistence after answers

| Write | Where |
|---|---|
| Chosen options | `workpapers/user_answers.json` + `workpapers/queries.md` → ## Answers |
| Soft-confirm accepted | `provisional` may stay true until openings fixed; log `soft_confirm: accepted` |
| Classification choices | Update `payee_map.json` + re-run `classify` / `post` / `tb` |
| Variance choices | Update journals (AR/AP/suspense/write-off) + re-run `tb` + refresh HTML |
| Limited vs full year | `engagement_type` + blockers |

Then re-run affected engine steps. **Never** only update chat.

---

## Anti-patterns (do not do)

1. Paste Tier-C questions only in a long status board  
2. “Let me know if anything looks wrong” without options  
3. Ten single payee questions instead of one batched structured ask  
4. Assume silence = accept (unless soft-confirm was already accepted earlier and logged)  
5. Clear `waiting_on_user` without a tool result or explicit letter reply  
6. **Dump an “Open queries” list as the main handoff** (homework mode)  
7. Ask “please confirm variance” without explaining what we booked and what each option does  
8. Mark engagement `done` while material variance themes were never put through the question tool  

---

## Skill checklist (for skills-qa)

When a skill says “ask the user”, verify it also says:

- [ ] Load `shared/user-questions.md`  
- [ ] Call structured question tool when available  
- [ ] Max 3 questions · options labeled · first = Recommended when known  
- [ ] Question text includes facts + what we booked + what choice changes  
- [ ] Persist answers to disk + re-run post/tb  
- [ ] Fallback ACTION REQUIRED block if no tool  
- [ ] Human pack is **HTML** (`outputs/*_pack.html`), not a pile of `.md` as the user UI  

---

## Version

`user-questions` doctrine **1.1** — 2026-07-09 (guided variance asks; no homework dumps).
