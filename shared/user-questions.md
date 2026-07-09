# User questions — structured tools required

**Problem this solves:** agents dump Tier-C asks into chat or `queries.md`, users never click through, work stalls or agents invent answers.

**Rule:** any question that **gates progress** or **needs a real choice** must use the host’s **structured user-question tool** when available — not prose alone.

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
| **Opening / prior year** | Provisional plug vs wait — only if openings block *their* goal |
| **User asked for full year-end but months missing** | Then ask: work limited period now vs wait for more months — **not** “you must supply 12 months” |
| **Blocker resolution** | User override of a hard gate (must be explicit) |
| **Finalisation / approval** | Management approval recorded |

**Do not** open with a deliverable quiz that implies full year is the only serious path.

## When prose / `queries.md` alone is OK

| Situation | Why |
|---|---|
| Status board only (no ask) | Informational |
| Long client query pack after structured asks already captured | Paper trail |
| Host has **no** question tool (see fallback) | Documented exception |
| Non-blocking FYI for staff later | Not a gate |

**Never:** only append to `workpapers/queries.md` and continue as if the user answered.

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
Question: Soft-confirm what I’m booking?
Options:
  - Accept: [Legal name] · [MYR] · banks cover [Jan–May 2026] · [bank]  (Recommended)
  - Fix entity name
  - Fix / narrow the period (e.g. only some months)
```

No “must supply full year” option. Depth of work is implied: we book **this period**.

### Upgrade to full year-end (only if user already asked for YE / FS)

```text
Question: Banks cover [Jan–May] only. How do you want to proceed?
Options:
  - Finish deep books for Jan–May now (Recommended) — TB, recon, ledger; label limited period
  - Pause books until I add more months (I will come back with files)
  - I want full-year FS later — keep going on Jan–May; I’ll add months when ready
```

**Wrong option (never use as recommended):** “You must provide all 12 months before we start.”

### Classification batch (1–3 questions, multi-select only if host supports)

```text
Question: PBB-PBCS AC 3 inflows (~RM 364k) — account?
Options:
  - 4000 Food & Beverage Sales (Recommended if customer/card settlement)
  - Other bank / float / clearing (not revenue)
  - Loan / financing proceeds
  - Suspense — need more docs
```

**Limits:**

- Max **3 questions** per tool call (matches smart-intake).
- Max **~5 options** per question.
- First option = **recommended** when you have a best guess; label it “(Recommended)”.
- Options must be **account codes + plain labels** for staff, or plain language for client.

---

## Workflow (mandatory order)

```text
1. Inventory + infer period coverage from files (truth matrix)
2. Extract / classify / post / TB for months present — do not wait
3. Soft-confirm via tool: entity + period-on-disk (≤1–2 asks if needed)
4. Write Hypothesis Card + queries.md (disk trail)
5. Persist answers; continue deeper work on that period
6. Full-year / FS / tax only when coverage + user intent support it
```

**While waiting on soft-confirm:** keep running extract/classify/post/tb for available months.  
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
| Chosen options | `engagement_state.notes` or `workpapers/queries.md` → ## Answers |
| Soft-confirm accepted | `provisional` may stay true until openings fixed; log `soft_confirm: accepted` |
| Classification choices | Update `payee_map.json` + re-run `classify` / `post` / `tb` |
| Limited vs full year | `engagement_type` + blockers |

Then re-run affected engine steps. **Never** only update chat.

---

## Anti-patterns (do not do)

1. Paste Tier-C questions only in a long status board  
2. “Let me know if anything looks wrong” without options  
3. Ten single payee questions instead of one batched structured ask  
4. Assume silence = accept (unless soft-confirm was already accepted earlier and logged)  
5. Clear `waiting_on_user` without a tool result or explicit letter reply  

---

## Skill checklist (for skills-qa)

When a skill says “ask the user”, verify it also says:

- [ ] Load `shared/user-questions.md`  
- [ ] Call structured question tool when available  
- [ ] Max 3 questions · options labeled  
- [ ] Persist answers to disk  
- [ ] Fallback ACTION REQUIRED block if no tool  

---

## Version

`user-questions` doctrine **1.0** — 2026-07-09.
