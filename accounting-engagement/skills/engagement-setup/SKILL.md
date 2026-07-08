---
name: engagement-setup
description: >
  Open or continue a client engagement after context is known: entity, FY,
  framework, COA, completeness, README + engagement_state.json. Trigger when
  starting year-end with known client details, "new client" with name given,
  or after smart-intake. If the user only dumped a folder with no company
  context, use smart-intake first — do not run a long blank questionnaire.
---

# /engagement-setup

## Purpose

Lock in engagement context **after** (or with) document-first discovery.

## Preconditions

1. `shared/guardrails.md`  
2. Firm profile if present (defaults only)  
3. **If folder dump / unknown entity** → run `smart-intake` first, then return here to formalize  

## Route

| Situation | Action |
|---|---|
| User gave legal name + period + clear docs | Setup directly (below) |
| User: “accounting for this folder” / no name | **`smart-intake` first** |
| `engagement_state.json` exists | `resume-engagement` |

## Workflow

### 1. Scan client folder
Banks, invoices, payslips, prior FS, SSM, tax files. Prefer facts from files over questions.

### 2. Entity identification
From SSM / bank account title / prior FS / smart-intake inferences:

- Legal name, registration number (only if on a doc — never invent)  
- Entity type  
- Address / activities if present  

Load `references/entity_types.md` or jurisdiction pack.

### 3. Framework selection (derive, don’t quiz)

| Entity | Framework | Tax form |
|---|---|---|
| Berhad (public) | MFRS | Form C |
| Sdn Bhd | MPERS | Form C |
| PLT | MPERS | Form PT |
| Sole prop | Accrual S21A | Form B |
| Partnership | Accrual S21A | Form P |
| Koperasi | MCA | Form TF |
| Trust | Varies | Form TP |

Only ask if entity type is still ambiguous after docs.

### 4. Financial year
Prefer statement date coverage + prior FS. Soft-confirm if incomplete year.

### 5. Completeness (honest, not scary)

**Blockers for full-year final FS:**

- Full-year bank statements (or accepted limited period)  
- Clear reporting entity identity  

**Not first-turn questions** — note as gaps:

- Payslips, FAR, inventory, loans, prior FS  

### 6. COA
Entity template + optional industry overlay from payee patterns (trading vs services). Soft default; user rarely needs to choose.

### 7. README + engagement_state.json

Per `references/engagement_state.schema.json` and `shared/agent-runtime.md`.

Include:

```markdown
## Inferences
| Field | Value | Confidence | Evidence |
```

### 8. Engagement card

```markdown
# Engagement: [Legal name]
- Entity / framework / tax form
- FY / coverage limitations
- Status: ready | provisional | blocked
- Next: extract banks → classify → …
```

## Question budget

After smart-intake, setup should usually ask **zero** new questions.  
If something critical is still open, ≤2 questions total.
