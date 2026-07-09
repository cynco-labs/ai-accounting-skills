---
name: bank-reconciliation
description: >
  Reconcile bank GL to statement at RM0. Use when bank recon or cash
  doesn't match.
---
# /bank-reconciliation

## Purpose

Prove cash. Tolerance: **RM0.00**.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



## Per bank account

1. Statement closing balance (date = FYE or recon date)
2. GL cash/bank closing balance
3. List outstanding deposits (in GL not statement)
4. List unpresented cheques / payments (in GL not statement)
5. Statement items not in GL (error → post correcting JE)
6. Reconciling formula:

```
Statement balance
+ deposits in transit
- outstanding payments
± errors corrected
= GL balance
```

7. Age outstanding items; flag > 3 months for investigation.

## Multi-account
Repeat for every current account, savings, foreign currency (note FX).


## Completion

**Done when:** per-bank recon on disk with difference 0.00 (or **AMBER**/blocker logged in state).

## Output
Bank recon schedule per account + combined cash note figure.  
**If not RM0.00 → BLOCKER.** Do not proceed to preliminary TB as clean.
