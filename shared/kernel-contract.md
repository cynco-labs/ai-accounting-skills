# Kernel contract — first principles

**Fewer nouns. One engine. Same or better proof.**

This document is the **source of truth** for what the product *is*.  
Skills, plugins, and CLI commands are delivery surfaces over this kernel — not parallel systems.

See also: `shared/skill-collapse-map.md` (36 → 6 intents), `shared/guardrails.md` (number integrity).

---

## Principles (non-negotiable)

1. **Every figure has a source** — path to document line, prior signed figure, or formula on those.
2. **Double entry** — each journal balances; trial balance DR = CR (minor unit).
3. **Bank is proof** — cash GL ties to statement (diff 0) or explicit AMBER limitation.
4. **Disk is truth** — chat is not the books; agents re-read artifacts after compaction.
5. **Present, don’t invent** — FS, tax, Excel, Beancount are *views* of locked balances.
6. **Human signs** — agent drafts; professional issues.

---

## Truth shapes (only these carry amounts)

Paths relative to `clients/<slug>/` (or any engagement root).

| Shape | Path | Role | Produced by |
|---|---|---|---|
| **State** | `engagement_state.json` | Stage, blockers, provenance meta — **not** balances | Agent + engine meta |
| **Evidence** | `source/**` + `source/register.md` | Immutable inputs | User / extract |
| **Lines** | `workpapers/transactions.json` | Bank (and other) lines + codes | `extract` → `classify` |
| **Journals** | `workpapers/journals.json` | Period double-entry (incl. openings) | `post` |
| **YE journals** | `workpapers/journals_ye.json` | Adjusting entries only | Agent judgment → same schema |
| **Balances** | `workpapers/tb_preliminary.json` | Reduce(period journals) | **`roll_tb` only** |
| **Balances** | `workpapers/tb_adjusted.json` | Reduce(period + YE journals) | **`roll_tb` only** |
| **Ledger SoR** | `ledger/main.beancount` | Final double-entry file | `export_to_beancount` after prove |
| **Presentation** | `outputs/fs/*`, tax, xlsx | Human packs from ATB map | `present` (no freestyle totals) |

Schemas: `references/schemas/{transactions,journals,trial_balance}.schema.json`.

### Derived vs authored

| May be authored by agent/human | Must be derived by engine (never typed as free totals) |
|---|---|
| Transaction classifications (after script + review) | Trial balance lines and totals |
| Journal lines (via `post` script or YE with balance check) | TB DR/CR columns from journals |
| YE journal catalogue decisions | Net account balances on TB |
| Note *wording* | FS line totals (must map from ATB) |
| Query / recon *narrative* | Beancount postings from journals |

**Rule:** If a script can compute it, the agent must not invent it in chat.

---

## Pure functions (engine)

Each function is **deterministic**, **idempotent** on the same inputs, and **fails loud**.

```text
extract(source_files) → transactions.json
  + balance proof meta
  scripts/extract_bank.py

classify(transactions, patterns, payee_map?) → transactions.json
  + classification_review.md
  scripts/classify_transactions.py

post(transactions, openings?, bank_code) → journals.json
  each JE balances or fail
  scripts/post_journals.py

roll_tb(journals…, kind) → tb_*.json
  pure reduce; DR=CR or fail
  scripts/roll_tb.py

export_ledger(journals + YE + map) → main.beancount
  bean-check
  scripts/export_to_beancount.py

prove(client_dir) → proof card | fail
  validate schemas + stage gates + optional ledger
  scripts/close_engagement.py
```

### `roll_tb` contract (critical)

**Input:** one or more `JournalBatch` JSON files (schema 0.0.1).  
**Output:** one `TrialBalance` JSON (`kind`: `preliminary` | `adjusted`).

Algorithm:

1. Reject any journal where Σ debit ≠ Σ credit (tolerance RM0.005).
2. Accumulate per `account_code`: sum debit, sum credit, last-seen `account_name`.
3. For each account, net to a single natural side (debit or credit column ≥ 0, other 0).
4. Totals: Σ line debits, Σ line credits; `difference` must be 0 or exit non-zero.
5. Sort lines by `account_code`.
6. Write JSON only — no chat, no Excel required.

**Preliminary TB** = `roll_tb(journals.json, kind=preliminary)`.  
**Adjusted TB** = `roll_tb(journals.json + journals_ye.json, kind=adjusted)`.

There is **no** separate TB “skill doctrine” beyond: run this function.

### `post` contract

**Input:** classified `transactions.json` (every in-scope row has `account_code`).  
**Output:** `journals.json` bank postings:

| Direction | Debit | Credit |
|---|---|---|
| inflow | bank GL | coded account |
| outflow | coded account | bank GL |

Optional openings file (same journal schema) is **prepended** (e.g. opening cash vs equity).  
Unclassified material lines → fail or suspense only if explicitly allowed.

---

## Kernel stages (5, not 16)

| Kernel stage | Meaning | Artifacts that must exist |
|---|---|---|
| `intake` | Entity / period / framework known or provisional | `engagement_state.json`, source register started |
| `books` | Lines coded and posted; prelim TB rolls | `transactions.json`, `journals.json`, `tb_preliminary.json` |
| `adjust` | YE journals considered; ATB rolls | `journals_ye.json` (may be empty pack), `tb_adjusted.json` |
| `present` | FS / notes / tax / workbook from ATB | `outputs/fs/*` as required by engagement type |
| `locked` | Prove + approval recorded; ledger SoR | proof card green, `ledger/main.beancount` if exported |

Legacy `current_stage` enum values in `engagement_state.schema.json` remain for compat; map them onto these five in orchestration docs. Prefer writing kernel stage in `notes` or a future `kernel_stage` field without breaking schema.

---

## Prove (definition of done)

`prove` / `close` succeeds only if:

1. Required artifacts for claimed progress exist (see `references/stage_artifacts.md`).
2. Every journal in scope balances.
3. Every TB present balances (`difference == 0`).
4. If recon claimed: bank diff documented as 0 (when recon validators land).
5. Optional: `bean-check` on ledger when exported.

Agents must not mark `status: done` without prove.

---

## What the agent still does (judgment only)

- Infer entity / period (smart intake) when docs allow  
- Resolve classification review queue  
- Choose YE adjustments (catalogue) and draft YE journal *lines* that `roll_tb` will accept  
- Draft note prose and client queries  
- Stop and ask on true blockers  

**Not** agent work: typing TB totals, balancing figures on BS, inventing bank lines.

---

## CLI surface (kernel verbs)

```bash
npx @cynco/accounting-skills extract …
npx @cynco/accounting-skills classify …
npx @cynco/accounting-skills post …      # → journals.json
npx @cynco/accounting-skills tb …        # → roll_tb preliminary / adjusted / both
npx @cynco/accounting-skills close …     # prove
npx @cynco/accounting-skills ledger …    # Beancount SoR
```

---

## Explicit non-goals (kernel)

- More stage plugins for the same transforms  
- Multiple COA copies as sources of truth (one pack path)  
- Connector / e-filing automation in the kernel  
- Vision freestyle extraction of banks  

---

## Version

Kernel contract version: **1.0** (aligned with engine scripts `post_journals.py`, `roll_tb.py`).  
Bump this section when pure-function signatures or truth shapes change.
