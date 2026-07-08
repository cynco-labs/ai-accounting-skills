<!--
CONFIGURATION LOCATION

User-specific configuration for this plugin lives at:

  ~/.claude/plugins/config/cynco-accounting-skills/reconciliation-accounting/CLAUDE.md

Rules for every skill in this plugin:
1. READ configuration from that path (not this template).
2. Also read shared firm profile: ~/.claude/plugins/config/cynco-accounting-skills/firm-profile.md
3. Read shared guardrails: ${CLAUDE_PLUGIN_ROOT}/../shared/guardrails.md or repo shared/guardrails.md
4. If firm profile is missing, offer /engagement-accounting:cold-start-interview (or provisional mode).
5. This file is the TEMPLATE. Never write live client data here.
-->

# Reconciliation Practice Profile

*Written/updated by cold-start or engagement setup. Edit in plain English — every skill reads this before doing work.*

---

## Who we are

**Firm:** [PLACEHOLDER — e.g. Hazli Johar & Co.]
**Registration:** [PLACEHOLDER — e.g. Chartered Accountants (NF1932)]
**Contact:** [PLACEHOLDER]

**Role of user:** [PLACEHOLDER — Partner | Manager | Senior | Associate | Bookkeeper]
**Partner sign-off required before:** [PLACEHOLDER — final FS issue | tax filing | auditor pack]

---

## Defaults

**Primary framework:** [PLACEHOLDER — MPERS for private entities]
**Currency:** MYR (RM)
**Capitalisation threshold:** RM2,000
**Depreciation policy:** [PLACEHOLDER — rates / method]
**Bank recon frequency:** [PLACEHOLDER — monthly | year-end only for compilation]
**Materiality (default):** RM100 line items may be grouped unless client-specific materiality set

---

## House style

**Working papers:** Excel multi-sheet workbook (scripts/generate_workbook.py)
**Client FS format:** Black & white, Helvetica/Arial, firm footer
**Comparative figures:** Required for MPERS/MFRS presentations
**Suspense policy:** Last resort after auto-classify + employee ask

---

## Escalation

| Situation | Action |
|---|---|
| Unbalanced TB | Stop — fix before FS |
| Missing full-year bank statements | Blocker — ask client |
| Related party uncertainty | Flag for partner |
| MPERS technical judgment | Partner / technical reviewer |
| Tax treatment ambiguity | Do not assume — document + escalate |

---

## Outputs

**Header on drafts:**
```
DRAFT FOR ACCOUNTANT REVIEW — NOT SIGNED FINANCIAL STATEMENTS
```

---

*Re-run firm setup: `/engagement-accounting:cold-start-interview --redo`*
