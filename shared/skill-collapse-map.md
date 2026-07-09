# Skill collapse map — 36 → 6 main jobs (frozen renames)

**Status:** frozen design. Do not invent new stage skills without updating this map.  
**Runtime:** older skill *names* may still install; new work targets the **six main jobs**.

In plain English: **do the books · extract · classify · post · present · prove**.  
(Install/code short names: `do-books`, `extract`, `classify`, `post`, `present`, `prove`.)

See `shared/kernel-contract.md` for standard work files and scripts. Plain terms: `CONTEXT.md`.

---

## The six main jobs

| Job | Plain English | Scripts / files | Human judgment |
|---|---|---|---|
| **do-books** | Start or continue the whole client job | state, status board | ≤3 questions; resume |
| **extract** | Source docs → proved lines | `extract_bank.py` → `transactions.json` | pick adapter / CSV vs PDF |
| **classify** | Lines → COA codes | `classify_transactions.py` + review list | confirm ambiguous payees |
| **post** | Coded lines (+ openings, YE) → journals; **TB is calculated** | `post_journals.py`, `roll_tb.py` | openings, YE catalogue lines |
| **present** | Adjusted TB → FS, notes, workbook, tax schedules | maps + templates; no hand-typed totals | disclosure wording |
| **prove** | QC, lock, export official ledger | `close_engagement.py`, `export_to_beancount.py`, Fava | approval to issue |

---

## Full map (legacy skill → intent)

### do-books

| Legacy skill | Action |
|---|---|
| `full-engagement-pipeline` | **Canonical** do-books body |
| `smart-intake` | Fold into do-books (section, not separate product) |
| `resume-engagement` | Fold: “read state and continue” |
| `engagement-setup` | Fold: write state + workspace |
| `client-workspace` | Fold: folder layout |
| `source-documents` | Fold: register + coverage |
| `cold-start-interview` | **Firm** only — keep separate install path or under builder; not client dump |

### extract

| Legacy skill | Action |
|---|---|
| `extract-bank-statement` | **Canonical** extract |
| `record-transactions` | Alias of extract (+ non-bank streams later as same intent) |

### classify

| Legacy skill | Action |
|---|---|
| `classify-transactions` | **Canonical** classify |
| `chart-of-accounts` | Precondition / data load for classify + post — not a pipeline stage |

### post

| Legacy skill | Action |
|---|---|
| `journal-entries` | **Canonical** post (run `post_journals.py`) |
| `year-end-adjustments` | post YE pack → `journals_ye.json` (same schema; balance-checked) |
| `preliminary-trial-balance` | **Deleted as doctrine** — `roll_tb --preliminary` only |
| `adjusted-trial-balance` | **Deleted as doctrine** — `roll_tb --adjusted` only |
| `bank-reconciliation` | Stays under post/prove until recon is a pure function; gate is still RM0 |
| `subledger-reconciliations` | Same: gate narrative under prove |

### present

| Legacy skill | Action |
|---|---|
| `prepare-primary-statements` | Canonical present (numbers from ATB map) |
| `prepare-notes` | present |
| `generate-workbook` | present |
| `compilation-report` | present |
| `mpers-technical-review` | present (standards judgment before/while FS) |
| `disclosure-checklist` | present subsection |
| `tax-computation` | present (from locked P&L / ATB) |
| `capital-allowances` | present subsection of tax |

### prove

| Legacy skill | Action |
|---|---|
| `quality-review` | Canonical prove checklist |
| `cross-tie-check` | **Fold into** quality-review / prove (no separate skill long-term) |
| `finalise-accounts` | prove + lock state |
| `management-approval` | prove gate field |
| `export-beancount` | prove → ledger SoR |
| `validate-beancount` | fold into export `--bean-check` |
| `open-fava` | UI after prove |
| `auditor-pack` | optional pack after prove |
| `statutory-handoff` | optional checklist after prove |

### builder only (not client engagement)

| Legacy skill | Action |
|---|---|
| `skills-qa` | builder |
| `jurisdiction-scaffold` | builder |
| builder `cold-start-interview` | firm profile (duplicate of engagement cold-start — consolidate later) |

---

## Rename freeze (target package names)

When a breaking major version collapses install surfaces, use these **only**:

```text
do-books
extract
classify
post
present
prove
```

Legacy names remain redirects in skill frontmatter `description` until major:

```yaml
# example future frontmatter
name: prove
alias_of: null
legacy_names: [quality-review, cross-tie-check, finalise-accounts, close]
```

Until then: **do not** add skills outside this map. Prefer engine scripts + kernel stages.

---

## Pipeline table (orchestrator)

Replace stage-skill soup with:

| # | Kernel | Intent | Command / script |
|---|---|---|---|
| 0 | intake | do-books | state + smart intake |
| 1 | books | extract | `extract` |
| 2 | books | classify | `classify` |
| 3 | books | post | `post` + `tb --preliminary` |
| 4 | adjust | post | YE journals + `tb --adjusted` |
| 5 | present | present | FS / notes / tax from ATB |
| 6 | locked | prove | `close` + `ledger` |

---

## Install guidance (simplified story)

**Agents need:** skills that cover the six intents (or full umbrella until collapse ships).  
**Humans/CI need:** `extract · classify · post · tb · close · ledger`.

Do not market 36 skills as the product. Market **folder → proved books**.

---

## Migration rules for contributors

1. New capability → which of the 6? If none, challenge the request.  
2. New *math* → pure function under `scripts/` + kernel-contract update.  
3. New *checklist* → section under prove/present, not a new skill.  
4. TB-related PRs that freestyle numbers → reject; use `roll_tb.py`.  
5. After editing a modular stage skill, run `python3 scripts/sync_umbrella.py`.

---

## Version

Collapse map version: **1.0**.  
Engine alignment: `post_journals.py`, `roll_tb.py` (kernel contract 1.0).
