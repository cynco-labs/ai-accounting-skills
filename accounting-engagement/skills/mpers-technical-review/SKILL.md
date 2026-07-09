---
name: mpers-technical-review
description: >
 Standards review before/with FS (MPERS/MFRS pack). Use when standards
 review or MPERS issues.
---
# /mpers-technical-review

## Purpose

Standards filter between ATB and FS drafting.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



Load `references/mpers.md` (and `mfrs.md` if framework is MFRS).

## Review programme (material balances)

For each area: **facts → standard section → conclusion → adj/disclosure/none**

1. **Revenue (S23)** — goods risks/rewards; services stage; construction; agency vs principal
2. **Leases (S20)** — finance vs operating classification; lessor/lessee disclosures
3. **Financial instruments (S11/S12)** — basic vs other; measurement; impairment of receivables
4. **Investment property (S16)** — cost model; classification vs PPE/inventory
5. **Inventories (S13)** — cost formula; NRV write-downs
6. **PPE (S17)** — capitalisation, componentisation if material, residual values, useful lives
7. **Intangibles (S18)** / goodwill (S19) — finite life amortisation under MPERS
8. **Impairment (S27)** — indicators; recoverable amount
9. **Employee benefits (S28)** — short-term, EPF defined contribution, termination
10. **Provisions & contingencies (S21)** — present obligation, probable, estimate
11. **Income taxes (S29)** — current + deferred if temporary differences material
12. **Related parties (S33)** — directors, shareholders, key management, common control entities
13. **Events after reporting period (S32)** — adjusting vs non-adjusting
14. **Going concern (S3)** — any doubt?
15. **Foreign currency (S30)** if applicable

## Materiality
Use engagement materiality; trivial items → disclosure only if specifically required.


## Completion

**Done when:** issues list on disk with severity; material items escalated or accepted with documentation.

## Output

```markdown
# MPERS Technical Review — [Client] FYE [date]

## Summary
- Further AJEs required: yes/no (list)
- Disclosure-only items: ...
- Partner attention: ...

## Detailed findings
### [Area]
**ATB amount:** ...
**MPERS ref:** Sxx
**Issue:** ...
**Recommendation:** Adjust JE-xxx | Disclose note X | Accept as is
**Evidence:** ...
```

Do **not** draft full notes here — hand findings to `prepare-notes` and any AJEs back to year-end if needed.
