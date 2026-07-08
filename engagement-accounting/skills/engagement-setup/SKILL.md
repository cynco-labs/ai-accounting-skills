---
name: engagement-setup
description: >
  Open a new or continuing Malaysian accounting engagement: identify entity, FY, framework, document completeness, COA template, and client README. Use when starting year-end, compilation, or bookkeeping for a client.
---

# /engagement-setup

## Purpose

Create a clean engagement context before any bookkeeping.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Workflow

### 1. Scan client folder
Identify available files: bank statements, invoices, payslips, prior FS, SSM extract, tax files.

### 2. Entity identification
From SSM Form 9/13/49, LLP cert, or client README:
- Legal name, registration number, entity type
- Directors / partners / proprietor
- Registered address
- Principal activities

Load `references/entity_types.md` (plugin or repo root).

### 3. Framework selection

| Entity | Framework | Tax form |
|---|---|---|
| Berhad (listed/public) | MFRS | Form C |
| Sdn Bhd | MPERS | Form C |
| PLT | MPERS | Form PT |
| Sole prop | Accrual S21A | Form B |
| Partnership | Accrual S21A | Form P |
| Koperasi | MCA | Form TF |
| Trust | Varies | Form TP |

### 4. Financial year
- FY start / end
- First year? comparative figures available?
- Prior year signed FS path

### 5. Completeness assessment

**Blockers (must resolve or log override):**
- Full-year bank statements (all accounts)
- Entity registration evidence

**Required when applicable:**
- Payslips / EA forms (payroll)
- Fixed asset invoices / register (PPE)
- Inventory listings (trading)
- Loan statements
- Prior year signed accounts (comparatives / openings)
- Sales & purchase invoices sample for classification

### 6. Load COA
Copy appropriate template from `bookkeeping-accounting/references/coa_templates/` or repo `references/coa_templates/`.

### 7. Write client engagement README
Use `references/client_readme_template.md`. Save under client workspace.

### 8. Output engagement card

```markdown
# Engagement: [Legal name]
- Entity type / framework / tax form
- FY: ...
- Status: Setup complete | Blocked (list)
- Next: /engagement-accounting:source-documents
```

If blockers → ask immediately. Do not pretend the engagement can complete.
