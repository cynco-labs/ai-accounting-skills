# Classify = substance → analysis → code

**First principle:** Codes are the end of classify. Understanding the money is the middle.

Scripts still own **amounts** and the trial balance.  
The agent owns **judgment under the reporting framework**, written into the folder.

See: `CONTEXT.md` · `shared/kernel-contract.md` · `bookkeeping-accounting/skills/classify-transactions/SKILL.md`

---

## The loop (always this order)

```text
1. Extract lines (proved balances)
2. Run classify script (baseline codes + review queue)
3. Build a money map (material themes: who / what / in or out)
4. For each material theme → load country-pack checklist
5. Ask only the hard questions (≤3 per theme, structured)
6. Write workpapers/analysis/<theme>.md
7. Set COA codes + payee_map from the conclusions
8. Re-run classify script → hand off to post
```

Do **not** jump from bank description to COA and call it done when the engagement is standards-aware.

---

## Engagement depth (`classify_depth`)

Store on `engagement_state.json` (optional field; free text in `notes` if schema is frozen for a client):

| Value | When | Behaviour |
|---|---|---|
| **`bookkeeping`** | Fast books only; user said “just code these” / light bookkeeping | Script + review queue + payee map. Analysis packs optional. |
| **`standards_aware`** | Default for **year_end**, **compilation**, “do classifications properly”, “revenue recognition”, material mixed banks | Full loop above. Material themes **must** have analysis packs. |

### How to choose (agent)

Depth follows **`engagement_type`**, not `operator`. Owners can still request year-end (`standards_aware`).

| Signal | Depth |
|---|---|
| `engagement_type` is `year_end` / `year_end_tax` / `compilation` | `standards_aware` |
| User: “do the classifications”, “revenue recognition”, “capitalise or expense”, “properly / according to MPERS” | `standards_aware` |
| User: “just categorise / quick books / bookkeeping only” | `bookkeeping` |
| Ambiguous folder dump aiming at year-end later | Prefer `standards_aware` once extract is done for that period |
| Tiny period, all pattern-clear payees, no material one-offs | `bookkeeping` is OK |

See also: `shared/operator-lens.md` (who drives vs how deep).

---

## Material themes (start here — not every line)

Build themes from **material** money, not from every Grab ride.

| Theme | Typical bank signal | Analysis file | Country checklist (MY) |
|---|---|---|---|
| Revenue | Material **credits** / money in from customers | `workpapers/analysis/revenue_recognition.md` | `references/jurisdictions/malaysia/standards/revenue_recognition.md` |
| Capital vs expense | Material **debits** / money out one-off or asset-like | `workpapers/analysis/capital_vs_expense.md` | `…/standards/capital_vs_expense.md` |
| PPE & depreciation | Capex concluded, or FAR present | `workpapers/analysis/ppe_and_depreciation.md` | (hooks in capital checklist + YE) |
| Related parties | Directors, shareholders, common names | `workpapers/analysis/related_parties.md` | MPERS S33 section in `mpers.md` |

**Materiality (default guide, not a statute):**

- Single line or same-payee cluster ≥ ~RM 500, **or**
- Statutory / payroll / tax / related party (any amount), **or**
- User or firm materiality if set

Below threshold: code via script/patterns; no analysis pack required.

---

## Analysis pack shape (every theme)

Use the template in `references/schemas/analysis_pack.example.md`. Minimum sections:

1. Scope & period  
2. What we saw (with sources)  
3. Standard applied (framework + section)  
4. Judgment  
5. Questions & answers  
6. Conclusion → COA codes / YE AJEs  
7. Open items  

**Done when (standards-aware):** every material theme either has a pack with a conclusion, or is listed as open query with reason.

---

## Relationship to later stages

| Stage | Role |
|---|---|
| **classify** (this doctrine) | First-pass substance + codes |
| **year-end adjustments** | Accruals, dep, cut-off that follow from analysis |
| **mpers-technical-review** | Second pass on the **ATB** — not the first place we “discover” revenue |
| **prepare-notes** | Pull wording from analysis packs where relevant |
| **quality-review** | Fail or **with limitation** if material revenue/capex lacks analysis |

---

## Thin aliases (same job, same folder)

User-invoked or rare triggers that only jump to a branch of classify:

- `revenue-recognition` → revenue theme only  
- `capitalise-or-expense` → capital vs expense theme only  

They do **not** invent a parallel pipeline. Outputs still under `workpapers/analysis/` and `transactions.json`.
