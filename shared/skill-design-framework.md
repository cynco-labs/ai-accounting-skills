# Accounting Skill Design Framework

Use this when writing or reviewing any `SKILL.md` in this marketplace.  
**Craft doctrine** (predictability, invocation, hierarchy, pruning): `shared/skill-craft.md`.  
**Domain language:** `CONTEXT.md`.  
`/accounting-builder-hub:skills-qa` evaluates skills against these criteria.

---

## 0. Craft gates (from skill-craft)

Before accounting criteria, the skill must clear craft:

| Check | Pass condition |
|---|---|
| Predictability | Same process every run; engine paths named for math |
| Invocation deliberate | Model-invoked only if agent must auto-fire; builder skills user-invoked |
| Description lean | Model-facing: front-loaded verb, one branch per trigger, no body-duplication |
| Steps or reference | Steps end on **checkable completion criteria**; pure-reference skills set an exhaustive bar |
| Hierarchy | Long catalogues disclosed via strong context pointer; doctrine not left to memory |
| Pruned | No no-ops, no duplicated meanings, no sprawl without disclosure |
| Positive steering | Prefer target behaviour; hard bans paired with what to do instead |
| Plain English | Prefer `CONTEXT.md` words over engineering slang in user-facing text |

---

## 1. Purpose clarity

- One skill = one job a senior associate would recognize on a timesheet.
- Name is a verb phrase or durable practice noun (`bank-reconciliation`, not `helper1`).
- Frontmatter `description`:
  - **Model-invoked:** when to use (distinct branches), not a restatement of the whole body.
  - **User-invoked:** one-line human summary; set `disable-model-invocation: true`; no trigger spam.
- Map the skill to a **main job** in `shared/skill-collapse-map.md`. Do not invent a seventh job without updating that map.

## 2. Preconditions

Every skill that produces numbers must:

1. Point at `shared/guardrails.md`
2. Load firm profile if present
3. Identify the active client / period / framework (or provisional path)
4. State what happens if sources are missing (**must stop** vs **with limitation** vs query)

## 3. Doctrine in the skill

Checklists, catalogues, and decision trees live **in the skill body** or a file the skill **always** loads with a strong pointer. Do not rely on model memory for:

- YE adjustment types  
- MPERS / framework section maps  
- Tax add-back categories  
- QC Section A blockers  

## 4. Gates

| Gate type | Example | Behavior |
|---|---|---|
| **Must stop** | TB DR ≠ CR | Stop; do not draft FS as final |
| Soft | Missing immaterial invoice | Query sheet; continue |
| Human approval | Issue signed FS | Wait for explicit confirmation |

Gates are **default-on**. Exemptions are narrow and logged on disk (`engagement_state` / queries).

## 5. Source of every figure

- Every material figure cites a source document, prior signed FS, or formula on sources.
- Calculations use tags: `[model calculation — verify]` when not a pure source extract.
- Never present example numbers as if they were the client’s.
- **TB only via `roll_tb`** — never type totals by hand in chat or Excel as the main ledger.

## 6. Outputs + completion

- Define the artifact (path under the engagement).
- Define the next skill / intent.
- Draft header unless the skill is post-approval issuance.
- Each step ends with a **completion criterion** that is checkable (and exhaustive where material).

Example:

```markdown
### Step 2 — Roll preliminary TB
…
**Done when:** `tb_preliminary.json` exists, `difference == 0`, and state stage advanced (or blocker recorded).
```

## 6b. User questions (when the skill asks)

If the skill tells the agent to ask the human anything that gates progress:

1. Point at `shared/user-questions.md`
2. Require the host **structured user-question tool** when available
3. Cap at ≤3 questions · labeled options · recommended first
4. Persist answers to `engagement_state` / `queries.md` / `payee_map`
5. Document fallback if the host has no tool

## 7. Failure modes

Document the top 3 ways the skill can go wrong and the required behavior:

| Failure | Required behavior |
|---|---|
| Missing bank month | **Must stop** or explicit **with limitation** note |
| Ambiguous payee | Structured ask (options); then suspense if still open |
| Standards judgment | Escalate; do not silently pick aggressive treatment |

Also watch craft failures: **premature completion**, **negation-only** steering, **sprawl**.

## 8. Trust surface

List what the skill may read/write:

- Client folder paths the user provides  
- Firm config under `~/.claude/plugins/config/claude-for-accounting/`  
- **Not** arbitrary home-directory scraping  
- **Not** external send (email, file-to-tax-portal) without explicit user action  

## 9. Extensibility

- Prefer jurisdiction-neutral stage logic + jurisdiction pack data.
- Prefer entity-neutral skill + COA/template selection.
- Industry specifics belong in overlays, not forked skills.

## 10. QA scorecard (for skills-qa)

Score each 0–2:

1. Purpose / triggers / invocation choice  
2. Preconditions  
3. Doctrine completeness  
4. Gates  
5. Source of every figure (+ roll_tb / scripts where math)  
6. Outputs + **Done when**  
7. Failure modes  
8. Trust surface  
9. Pipeline / main-job position  
10. No firm lock-in / no fabricated numbers  
11. **Craft** — lean description, hierarchy, pruning, positive steering, plain English  

If the skill asks the user anything that gates progress, also require: points at `shared/user-questions.md`, structured tool when available, ≤3 options-shaped asks.

**Ship bar:** ≥ 18/22 and **no zero** on gates (4), source-of-figure (5), or craft (11) when the skill produces numbers.
