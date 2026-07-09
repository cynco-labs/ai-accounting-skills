---
name: source-documents
description: >
 Register sources and bank coverage. Use when source register or document
 inventory.
---
# /source-documents

## Purpose

Build a complete source-document inventory and readiness score before recording transactions.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Document categories to inventory

| Category | Examples | Notes |
|---|---|---|
| Bank | Monthly statements, e-statements, FD | Continuity: no missing months |
| Sales | Invoices, credit notes, POS, contracts | Match deposits where possible |
| Purchases | Supplier invoices, credit notes | Match payments |
| Payroll | Payslips, EA, PCB, EPF/SOCSO listings | Net pay ↔ bank |
| PPE | Purchase invoices, disposal docs, FAR | Capitalisation threshold |
| Loans | Facility letters, statements, schedules | Interest vs principal split |
| Tax | Prior CT, CP204, assessments | b/f losses, CA c/f |
| Statutory | SSM, Form 24/44/49, constitution | Name consistency |
| Prior year | Signed FS, TB, working papers, tax comp | Opening balances authority |
| Other | Stock take, tenancy, related party list | YE estimates |

## Workflow

1. List every file in the client folder (name, type, period covered).
2. Build a **coverage matrix** (document type × month or YE).
3. Verify bank statement continuity (opening of month N = closing of N−1).
4. Flag duplicates and unreadable scans.
5. Score readiness:
 - **Green** — can bookkeep fully
 - **Amber** — can proceed with listed limitations
 - **Red** — blockers (missing banks / entity / openings)


## Completion

**Done when:** `source/register.md` lists files with coverage matrix; gaps are **must stop** or **with limitation**.

## Output

```markdown
# Source Document Register — [Client] FY[year]

## Coverage matrix
...

## Gaps & client requests
1. ...

## Readiness: GREEN | AMBER | RED
## Next skill: /bookkeeping-accounting:record-transactions
```

Update client README. Do not invent missing documents.
