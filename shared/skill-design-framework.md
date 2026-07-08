# Accounting Skill Design Framework

Use this when writing or reviewing any `SKILL.md` in this marketplace.
`/accounting-builder-hub:skills-qa` evaluates skills against these criteria.

## 1. Purpose clarity

- One skill = one job a senior associate would recognize on a timesheet.
- Frontmatter `description` states **when to use** (triggers), not only what it is.
- Name is a verb phrase or durable noun used in practice (`bank-reconciliation`, not `helper1`).

## 2. Preconditions

Every skill that produces numbers must:

1. Point at `shared/guardrails.md`
2. Load firm profile if present
3. Identify the active client / FY / framework
4. State what happens if sources are missing (block vs provisional vs query)

## 3. Doctrine in the skill

Checklists, catalogues, and decision trees live **in the skill body** (or a `references/` file the skill explicitly loads). Do not rely on model memory for:

- YE adjustment types
- MPERS section maps
- Tax add-back categories
- QC Section A blockers

## 4. Gates

| Gate type | Example | Behavior |
|---|---|---|
| Blocker | TB DR ≠ CR | Stop; do not draft FS as final |
| Soft | Missing immaterial invoice | Query sheet; continue |
| Human approval | Issue signed FS | Wait for explicit confirmation |

Gates are **default-on**. Exemptions are narrow and logged.

## 5. Provenance

- Every material figure cites a source document, prior signed FS, or formula on sources.
- Calculations use tags: `[model calculation — verify]` when not a pure source extract.
- Never present example numbers as if they were the client’s.

## 6. Outputs

- Define the artifact (memo, schedule, workbook sheet, checklist).
- Define the next skill in the pipeline.
- Draft header unless the skill is post-approval issuance.

## 7. Failure modes

Document the top 3 ways the skill can go wrong and the required behavior:

| Failure | Required behavior |
|---|---|
| Missing bank month | Blocker or explicit AMBER limitation |
| Ambiguous payee | Ask employee; then suspense |
| Standards judgment | Escalate; do not silently pick aggressive treatment |

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

1. Purpose / triggers  
2. Preconditions  
3. Doctrine completeness  
4. Gates  
5. Provenance  
6. Outputs  
7. Failure modes  
8. Trust surface  
9. Pipeline position  
10. No firm lock-in / no fabricated numbers  

**Ship bar:** ≥ 16/20 and no zero on gates or provenance.
