# Slash surface — short commands, long bodies

Make the **user-facing** skill menu short and stable (like a well-designed CLI).  
Keep **implementation** in one canonical skill per job. Aliases never copy doctrine.

---

## First principles

1. **Six public verbs** — `do-books` · `extract` · `classify` · `post` · `present` · `prove`  
2. **Thin aliases only** — short `SKILL.md` loads the canonical skill; no second copy of steps  
3. **User vs model**  
   - **User-invoked** short names (`disable-model-invocation: true`) → what humans type  
   - **Model-invoked** long names (rich `description`) → auto-routing from natural language  
4. **Front door** — natural language “do the accounting” or `/do-books`. `/ask-accounting` is **optional** (lost users only), not the default.  
5. **No sprawl** — do not add a short slash unless it is a main job, the optional router, or a rare high-value branch already on the collapse map  
6. **One product, two axes** — `operator` (owner | bookkeeper | firm) + depth (`engagement_type` / `classify_depth`). Same slashes for everyone. See `shared/operator-lens.md`. **Never** add `/accounting4business` vs `/accounting4firm`.  
7. **Runtime brief** — agents load `shared/runtime-brief.md` first, not a pile of doctrine files.

---

## Public menu (what users learn)

### Main jobs (type these)

| Slash / skill name | Meaning | Canonical body |
|---|---|---|
| **do-books** | Start or continue the whole engagement | `full-engagement-pipeline` |
| **extract** | Banks / sources → proved lines | `extract-bank-statement` |
| **classify** | Substance (if needed) → COA codes | `classify-transactions` |
| **post** | Journals + calculated TB | `journal-entries` |
| **present** | FS / notes from adjusted TB | `prepare-primary-statements` (+ notes as needed) |
| **prove** | QC / lock path | `quality-review` |

### Helpers

| Slash / skill name | Meaning | Canonical body |
|---|---|---|
| **resume** | Continue from `engagement_state.json` | `resume-engagement` |
| **revenue** | Revenue recognition branch | `revenue-recognition` → classify |
| **capex** | Capitalise vs expense branch | `capitalise-or-expense` → classify |
| **ask-accounting** | Optional menu if lost | Router only — **not** the default entry |

### How they appear by host

| Host | What you type |
|---|---|
| **skills.sh / flat install** | `/do-books`, `/classify`, … (skill `name`) |
| **Claude Code plugin (umbrella)** | `/accounting-engagement:do-books`, … |
| **Natural language** | “Do the accounting” → model still reaches **long** skills via descriptions |

Never tell clients a wall of long stage names. Staff can learn the **six verbs**.

---

## Maintenance rules

| Do | Don’t |
|---|---|
| Edit doctrine only in the **canonical** skill | Paste the full pipeline into `do-books` |
| Keep alias body under ~40 lines | Grow aliases into real workflows |
| Update this table when adding a public slash | Invent `/helper12` outside the collapse map |
| Point aliases at paths relative to repo / plugin | Deep-link brittle absolute paths only |

When the collapse map’s rename freeze ships, long install names become legacy redirects; **public verbs stay**.

---

## Agent behaviour when a short slash is used

1. Resolve canonical skill (table above).  
2. Read that skill’s `SKILL.md` fully.  
3. Execute until its **Done when** (or must stop).  
4. Do not also freestyle a parallel process.  

If the user types `/ask-accounting`, interview once and recommend **one** short slash (and optional follow-ups).

---

## Scalability

```text
Users remember:     “do the accounting” + optional 6 verbs
Model discovers:    long skill descriptions (auto)
Maintainers edit:   one canonical body per job
Country packs:      data under references/jurisdictions/ — not new slashes
```

New country ≠ new slash.  
New bank adapter ≠ new slash.  
New disclosure note template ≠ new slash.  
New audience (owner vs firm) ≠ new slash — set `operator` on state / firm profile.  
New **main job** = update collapse map first, then add a short alias.
