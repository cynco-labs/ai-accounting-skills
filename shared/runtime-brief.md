# Runtime brief — load this first (one screen)

**Throw-work default.** Deep doctrine only when a step needs it.

| Need more detail | Open |
|---|---|
| Amounts / TB / files | `shared/kernel-contract.md` |
| Six jobs map | `shared/skill-collapse-map.md` |
| Organize messy docs | `shared/shelf-first.md` |
| Owner vs firm | `shared/operator-lens.md` |
| Questions UI | `shared/user-questions.md` |
| Classify judgment | `shared/classify-substance.md` |
| Words | `CONTEXT.md` |

---

## Front door

User says **“do the accounting”** / throws a folder / types `/do-books`  
→ this pipeline. **Not** cold-start. **Not** `/ask-accounting`.

Agents run scripts quietly (`npx @cynco/accounting-skills …` or `python3 scripts/…`).  
Users see plain progress — not command school.

---

## Order (one intake, then books)

```text
1. RESUME?  engagement_state.json → continue (skip re-intake)
2. INTAKE   one pass: discover → shelf → register → state → ≤3 asks
3. BOOKS    extract → classify → post → recon → TB   [default stop]
4. DEEPER   YE / standards / FS / QC / tax   only if engagement_type needs it
5. LEDGER   Beancount + Fava when books balance (or user asks)
```

**Never** re-run shelf + setup + source-documents as three separate user-facing ceremonies.

---

## Hard rules (always)

1. No invented numbers — re-read files after context loss  
2. TB only via `roll_tb` / `npx … tb`  
3. Bank recon **0** or clear **with limitation**  
4. Files on disk are the books  
5. Progress asks → structured question tool (`shared/user-questions.md`) — **no open-query homework dumps**  
6. Work the months on disk — don’t demand 12 months  
7. Human pack = **HTML** (`outputs/*_pack.html`), not a pile of markdown  

---

## Operator + depth (on state)

| Field | Values | Default (folder dump) |
|---|---|---|
| `operator` | owner · bookkeeper · firm | infer; else one ask |
| `engagement_type` | bookkeeping_only → year_end_tax | **bookkeeping_only** |
| `classify_depth` | bookkeeping · standards_aware | follows type |

---

## Done when (depth-scoped) — critical UX

**Machine truth:** `references/depth_gates.json` · `python3 scripts/depth_gates.py <client> --strict`

| `engagement_type` | Stop when depth gates pass | Do **not** force |
|---|---|---|
| **bookkeeping_only** | register · txns · journals · bank recon · prelim TB | YE, FS, notes, full QC, tax |
| **compilation** / **year_end** | books + YE · adjusted TB · primaries · notes · QC A | Tax unless asked |
| **year_end_tax** | year-end + tax computation | — |
| User: “stop after TB” | Honor; write state | — |

Mark `status: done` only after **depth-scoped prove** (`close` / `depth_gates --strict`).  
Partial path → `in_progress` or clean stop — never fake year-end complete.

---

## Status board (human-facing = six jobs)

Show **jobs**, not 16 internal stage keys. Warm, specific, next action clear:

```markdown
## Acme Sdn. Bhd. · Jan–May 2026 · books only
| Step | Status | Notes |
|---|---|---|
| Organize | Done | Folder ready · register saved |
| Extract | Done | 412 bank lines |
| Classify | Needs you | 6 payees — pick accounts |
| Post | Next | Journals + trial balance |
| Present | HTML pack ready | outputs/*_pack.html |
| Prove | Later | After books balance |

**I need from you:** answers on the 6 payees (options above).
**Next from me:** post and trial balance once those are set.
**Read:** open the HTML pack — not a stack of .md files.
```

Internal `current_stage` may stay fine-grained for resume; **don’t dump stage keys at owners**.

### Human pack rule

| Audience | Deliverable | Not the user UI |
|---|---|---|
| Owner / bookkeeper / firm review | **`outputs/<slug>_pack.html`** (open in browser) | Raw `README.md`, `queries.md`, TB `.md` alone |
| Machine / resume | `workpapers/*.json` + `engagement_state.json` | — |
| Deep staff review | Excel working papers (optional) | — |
| Interactive books | Fava on Beancount | — |

After books steps, **generate or refresh HTML** (`scripts/generate_html_report.py`).  
**Prove fails** without a fresh `outputs/*_pack.html` (`depth_gates` · `html_pack`).  
`.md` files stay as **staff/disk trail**, not the primary handoff.  
**Fava** = optional explore of Beancount — not the handoff, not the truth.

---

## Intake checklist (single pass)

1. Discover cwd + user paths (no home crawl)  
2. Job map if multi-entity → pick active job  
3. `clients/<slug>/` + place sources → `source/register.md`  
4. Set `operator`, `engagement_type`, provisional OK  
5. Soft-confirm entity + period-on-disk (one question)  
6. Start extract from shelf **same session**  

Doctrine if stuck: `shared/shelf-first.md` · `shared/smart-intake.md`.

---

## Scripts (agent runs; user doesn’t need to type)

```bash
npx @cynco/accounting-skills extract <source> --json workpapers/transactions.json
npx @cynco/accounting-skills classify workpapers/transactions.json
npx @cynco/accounting-skills post <client> --opening-from-bank
npx @cynco/accounting-skills tb <client> --both
npx @cynco/accounting-skills close <client>    # prove path
npx @cynco/accounting-skills ledger <client>
```

---

## Load more only when

| Situation | Then load |
|---|---|
| Messy multi-path dump | `shared/shelf-first.md` |
| Soft-confirm / classify / variance ask | `shared/user-questions.md` |
| Human-readable pack | `shared/html-deliverables.md` · `scripts/generate_html_report.py` |
| Year-end / “properly” | `shared/classify-substance.md` |
| Producing FS numbers | `shared/guardrails.md` + kernel |
| Firm missing + client work | firm profile / cold-start **once** |

**Default throw-work:** this brief + active stage skill body + firm profile if present.  
**Not default:** loading 10 doctrine files before the first PDF.
