# Operator lens — one engine, two axes

**Same math. Same six jobs. Same work files.**  
What changes is **who is driving** and **how deep** we go — not which product we are.

See: `CONTEXT.md` · `shared/kernel-contract.md` · `shared/slash-surface.md` · `shared/smart-intake.md`

---

## First principles

1. **One public door** — `/do-books` (or “do the accounting”). No `/accounting4business` vs `/accounting4firm` forks.
2. **Two axes only** — store both on `engagement_state.json`:
   - **`operator`** — who is driving (copy, questions, branding, who signs)
   - **`engagement_type`** — how deep (books → management → year-end → tax)
3. **Scripts ignore the lens** — extract / classify / post / `roll_tb` / close do not branch on operator. Numbers stay identical.
4. **Skills adapt at the edges** — language, default depth, deliverable set, stop-lines, letterhead.
5. **Infer → soft-confirm → ask once** — never open with “are you a firm?” if evidence is clear.

---

## Axis A — `operator`

| Value | Who | Voice | Branding | Typical default depth |
|---|---|---|---|---|
| **`owner`** | Founder / director / sole prop doing **their own** books | Plain English; no stage jargon | No firm letterhead unless they set one | `bookkeeping_only` |
| **`bookkeeper`** | In-house or outsourced bookkeeper | Clear process; light codes | Optional practice name | `bookkeeping_only` → upgrade on request |
| **`firm`** | Practice staff on a **client** job | Technical where useful; staff vs client voice | Firm profile letterhead / footer | As engagement letter / ask |

### Resolve `operator` (order)

```text
1. engagement_state.operator if already set → keep
2. firm-profile “Default operator:” if set → use
3. Soft-infer:
   - Real firm profile present (not PLACEHOLDER) + user talks about “the client” / multi-client → firm
   - Personal-name bank account, “my books / my company”, no firm profile → owner
   - “I’m the bookkeeper for …” → bookkeeper
4. Still unclear → ONE structured question (see below). Save answer to state.
```

**Do not** re-ask every session. Resume from state.

### Soft-ask (only when Tier C)

Use structured tool (`shared/user-questions.md`):

```text
Question: Who is this work for?
- My own business / personal company (Recommended when personal folder dump)
- I’m a bookkeeper for this entity
- Client work for our accounting firm
```

Max one of the ≤3 intake questions when needed.

---

## Axis B — depth (`engagement_type` + `classify_depth`)

Depth is **already** on state. Do not invent a third enum.

| `engagement_type` | Meaning | Default `classify_depth` | Present / prove target |
|---|---|---|---|
| **`bookkeeping_only`** | Books for period on disk | `bookkeeping` | TB, recon, ledger; simple P&L/BS optional DRAFT |
| **`compilation`** | Compile FS for client | `standards_aware` | Primary statements + notes + QC |
| **`year_end`** | Full year-end pack | `standards_aware` | FS + notes + QC + lock path |
| **`year_end_tax`** | Year-end + tax | `standards_aware` | Above + tax from locked figures |
| **`audit_support`** | Auditor pack support | `standards_aware` | Workpapers + ties; not an audit opinion |
| **`unknown`** | Not set yet | Prefer `bookkeeping` until upgrade | Period books only |

Upgrade depth when the user asks (year end / FS / tax) **and** coverage supports it — see period-on-disk rules.

---

## Lens matrix (what agents change)

| Concern | `owner` | `bookkeeper` | `firm` |
|---|---|---|---|
| Status board | “What I’m doing / what I need from you” | Stage + blockers | Full stage table OK |
| Questions | Plain; no COA codes unless they want them | Codes OK | Staff = codes; client lists = plain |
| Default engagement_type (folder dump) | `bookkeeping_only` | `bookkeeping_only` | `bookkeeping_only` unless they said year end |
| Draft header | “DRAFT — for your review” | “DRAFT — for review” | “DRAFT FOR ACCOUNTANT REVIEW” + firm name |
| Firm cold-start | Skip unless they want branding | Optional | Offer once if profile missing |
| Final “signed FS” language | Never claim issued FS | Same | Same + partner gate from firm profile |
| Present default | Simple P&L / cash / “send to accountant” pack | Workpapers + TB | Full FS path when depth says so |
| Prove default | TB balance + bank recon + optional ledger | Same + review list | QC Section A before “final” |

**Unchanged for all operators:** no invented numbers · TB only via `roll_tb` · bank recon 0 · files are the books · six jobs.

---

## Public UX (stable)

| User types / says | What happens |
|---|---|
| `/do-books` · “do the accounting” | Resolve operator + depth → same pipeline |
| `/extract` … `/prove` | Power path — same for everyone |
| Firm first install | `cold-start-interview` → firm-profile + optional `Default operator: firm` |
| Owner never installs firm profile | `operator: owner`, provisional branding OK |

**Do not** add audience-specific short slashes.  
New country / bank / note template ≠ new operator.  
New main job still goes through `shared/skill-collapse-map.md` first.

---

## State fields

```json
{
  "operator": "owner",
  "engagement_type": "bookkeeping_only",
  "classify_depth": "bookkeeping"
}
```

Schema: `references/engagement_state.schema.json`  
Write both at smart-intake / engagement-setup; never leave operator blank after first resolution.

---

## Anti-patterns

| Don’t | Do |
|---|---|
| Fork skills into business vs firm trees | One skill body + lens table |
| Assume firm because the repo is “engagement-shaped” | Infer operator; default owner on personal dumps |
| Teach two slash menus | One menu; profile/state holds the lens |
| Change post/TB math by operator | Change copy and gates only |
| Re-interview operator every resume | Read state |

---

## Done when (for agents applying the lens)

- [ ] `operator` and `engagement_type` set on disk  
- [ ] Voice and deliverables match the matrix above  
- [ ] Scripts and work files identical regardless of operator  
- [ ] User was not forced into a firm questionnaire for a personal folder dump  
