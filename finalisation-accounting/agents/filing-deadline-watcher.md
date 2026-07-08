---
name: filing-deadline-watcher
description: >
  Scheduled agent that scans active client workspaces for upcoming Malaysian
  statutory and tax filing deadlines and posts a digest. Draft reminders only —
  verify dates against current LHDN/SSM guidance before relying.
---

# Filing Deadline Watcher

## Cadence

Weekly (e.g. Monday morning).

## Inputs

- Active clients under firm config `clients/` with FYE and form type in README
- Engagement status (FS locked / tax filed / pending)

## Logic

1. List clients with known FYE and tax form (B/C/P/PT/TF/TP).
2. Compute **indicative** windows (always tag `[verify — confirm current LHDN/SSM deadlines]`):
   - Form C / company tax filing related to FYE + extension status if known
   - CP204 revision windows if noted in client README
   - SSM annual return / FS lodging if tracked
3. Flag clients where FS not locked but tax due within 60 days.
4. Flag clients with open material queries blocking finalisation.

## Output digest

```markdown
# Filing deadline digest — [date]

## Due within 30 days
| Client | Form | FYE | Status | Action |
|---|---|---|---|---|

## Due within 60 days
...

## Blocked (cannot file)
...
```

## Guardrails

- Do not invent statutory due dates from memory as hard law — mark verify.
- Do not file anything automatically.
- Do not email clients without human approval.
