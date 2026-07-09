# Skill craft — how we write skills that behave

Doctrine for every `SKILL.md` in this marketplace.  
Pair with `shared/skill-design-framework.md` (accounting scorecard) and `shared/kernel-contract.md` (truth shapes).  
`/accounting-builder-hub:skills-qa` scores craft and accounting gates together.

---

## Root virtue: Predictability

A skill exists to wrangle **determinism of process** out of a stochastic model.

- Same *process* every run — not the same output.
- Brainstorming may diverge; bookkeeping must not freestyle a TB.
- Every lever below serves predictability. Token cost and maintainability are symptoms.

---

## Axis 1 — Invocation (who can reach the skill)

| Kind | Frontmatter | Description job | Load paid |
|---|---|---|---|
| **Model-invoked** | omit `disable-model-invocation` | Model-facing: what it is + **distinct trigger branches** | **Context load** — description always in the window |
| **User-invoked** | `disable-model-invocation: true` | Human-facing one-liner; **no** trigger lists | **Cognitive load** — human must remember it |

Rules:

1. Model-invoke only when the agent must fire it alone **or** another skill must reach it.
2. User-invoke builder/meta work, rare ops, and anything that should never auto-start mid-engagement.
3. A user-invoked skill may invoke model-invoked skills; it cannot fire another user-invoked skill (no description → no agent reach).
4. When user-invoked skills pile up, ship a **router skill** (one name that maps situations → skills). Ours: `full-engagement-pipeline` (do-books) for engagements; `skills-qa` stays user-invoked.

### Description craft (model-invoked)

- **Front-load the leading verb** (`Extract…`, `Classify…`, `Prove…`).
- **One trigger per branch** — synonyms that rename the same branch are duplication; collapse them.
- Cut identity already in the body. Triggers + optional “when another skill needs…” only.
- Prefer **≤ 400 characters** when possible. Long descriptions tax every turn of every chat.
- Target the **6 intents** (`do-books · extract · classify · post · present · prove`) as the long-term discoverable set; legacy names stay as aliases in body until major collapse.

### Default invocation map (this marketplace)

| Bucket | Default | Examples |
|---|---|---|
| Engagement stage skills | **Model-invoked** | extract, classify, journal-entries, bank-reconciliation, quality-review |
| Orchestrator | **Model-invoked** (router) | full-engagement-pipeline, smart-intake, resume-engagement |
| Builder / contributor | **User-invoked** | skills-qa, jurisdiction-scaffold, builder cold-start |
| Destructive / issuance | Prefer **user-invoked** or hard human gate in body | finalise-accounts (gate), statutory external send |

---

## Axis 2 — Information hierarchy

Rank content by how immediately the agent needs it:

1. **In-skill steps** — ordered actions; each ends on a **completion criterion**
2. **In-skill reference** — rules/facts consulted on demand (flat peer-sets OK)
3. **Disclosed reference** — sibling file under the skill, or repo `references/` / `shared/`, loaded only when a **context pointer** fires

**Progressive disclosure:** push what only some **branches** need behind a pointer; keep what every path needs inline.

**Co-location:** definition + rules + caveats for one concept under one heading.

**Context pointer wording** decides reliability — a weak “see also X” is a variance bug; sharpen wording before inlining.

### Doctrine rule (accounting-specific)

Load-bearing catalogues (YE adjustments, QC Section A, tax add-backs) must be **in the skill or an explicit pointer the skill always fires** — never “rely on model memory.”  
That is progressive disclosure of *reference*, not abdication of doctrine.

---

## Axis 3 — Steering (runtime behaviour)

### Leading words

Compact tokens already in model priors (or defined once in `CONTEXT.md` / kernel) that anchor behaviour:

| Leading word | Behaviour it steers |
|---|---|
| **kernel** | Use pure functions / scripts; do not freestyle math |
| **roll_tb** | TB is derived only; never type totals |
| **period-first** | Book months on disk deeply; do not stall for 12 months |
| **disk is truth** | Re-read artifacts after compaction; chat is not the books |
| **blocker** | Hard stop; do not present as final |
| **AMBER** | Documented limitation; continue only where allowed |
| **provenance** | Every material figure has a source tag |
| **structured ask** | Progress questions via host question tool ≤3 |
| **tracer bullet** | Vertical slice: one complete path, demoable alone |
| **completion criterion** | Checkable done condition for a step |

Repeat the **token**, not a restated paragraph. Weak words (`be thorough`) are **no-ops** — use stronger ones (`relentless`, `every Section A item`).

### Completion criteria

Every step ends with a condition that is:

- **Checkable** — agent can tell done from not-done
- **Exhaustive where it matters** — “every material `needs_review` row resolved or queried”, not “review some rows”

Vague criteria invite **premature completion** (attention slips to the next stage).

### Negation vs positive

Prefer **positive target behaviour**:

- Weak: “Do not invent TB totals”
- Strong: “TB only via `roll_tb.py`; difference must be 0”

Hard guardrails that cannot be phrased positively stay, **paired** with what to do instead.

### Premature completion defence

1. Sharpen the completion criterion (cheap, local).
2. Only if still fuzzy *and* you observe rush: split the sequence so post-completion steps leave context (separate skill / subagent / user-invoked handoff).

Orchestrators (`full-engagement-pipeline`) **must** load one stage skill at a time — not paste the whole pipeline into context.

---

## Axis 4 — Pruning

| Failure | Meaning | Cure |
|---|---|---|
| **Duplication** | Same meaning in two places | Single source of truth |
| **Sediment** | Stale layers never removed | Relevance pass before merge |
| **Sprawl** | Too long even when live | Disclose reference; split by branch/sequence |
| **No-op** | Model already does it by default | Delete the sentence |
| **Negation** | Pink-elephant bans | Positive target + hard gate only if needed |

**No-op test (per sentence):** does this change behaviour vs the default agent? If not, delete the whole sentence.

---

## Design → write → execute

### Design

1. Name the **timesheet job** and which **intent** it sits under (collapse map).
2. Choose **invocation** (model vs user).
3. List **truth shapes** read/written (`kernel-contract.md`).
4. List **gates** (blocker / soft / human).
5. List **branches** (folder dump vs resume vs single-stage).
6. Pick **leading words**; avoid inventing jargon that isn’t in `CONTEXT.md`.

### Write

1. Frontmatter: `name`, craft-worthy `description`, optional `disable-model-invocation`.
2. Steps with completion criteria **or** flat reference with exhaustive bar.
3. Point at `shared/guardrails.md` for number skills.
4. Disclose long catalogues to `references/` with a strong pointer.
5. Failure modes table (top 3).
6. Prune: no-op, duplication, sprawl.

### Execute (agent runtime)

1. Load skill → run steps → write disk artifacts → update `engagement_state.json`.
2. Hit completion criterion before advancing.
3. On blocker: stop with status board + structured ask if needed.
4. Prefer engine scripts over chat freestyle for extract / classify / post / roll_tb / close.

### QA

Run `/accounting-builder-hub:skills-qa` (or score manually) against the framework scorecard + craft checks.

---

## Anti-patterns we refuse

| Anti-pattern | Why |
|---|---|
| 30+ always-on model skills with novel essays for descriptions | Context load; agent can’t choose |
| Stage skill with no completion criterion | Premature jump to FS |
| Doctrine only in CLAUDE.md | Skill collapses without the net |
| “Don’t fabricate” without engine path | Negation without positive procedure |
| Horizontal “do all stages” in one context | Premature completion; fog of war lost |
| New stage skill outside collapse map | Sprawl of product surface |
