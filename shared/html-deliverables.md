# HTML deliverables (human pack)

## First principle

Users open **one page** and understand:

1. Is the work solid?  
2. What do **I** need to do?  
3. What was booked?

They are **not** sent a stack of markdown files as the handoff.

| Layer | Path | Role |
|---|---|---|
| **Human pack** | `outputs/<slug>_pack.html` | Default readable deliverable |
| Machine truth | `workpapers/*.json` | Scripts, resume, gates |
| Optional override | `workpapers/action_items.json` | Richer checklist items |
| Disk trail | `README.md`, `workpapers/*.md` | Staff notes only |
| Working papers | `outputs/*.xlsx` | Optional deep dive |
| Ledger UI | Fava | Interactive |

## Fixed layout (always the same — **board, left → right**)

This is a **horizontal board**, not a long essay you scroll top→bottom.

```
Header (identity) ……………………………… DRAFT
Progress: 1 → 2 → 3 → 4 → 5 → 6
┌──────────────┬──────────────┬────────────────┐
│ ACTION       │ AT A GLANCE │ WHAT WE BOOKED │
│ checklist    │ + decisions  │ + trial balance│
├──────────────┴──────────────┴────────────────┤
│ Sales vs bank  →  │  Supplier bills vs bank  │
└──────────────────────────────────────────────┘
```

| Zone | Position | Content |
|---|---|---|
| Progress | Top strip LTR | Six jobs Organize → Prove |
| **Actions** | **Left column** | Checklist: Why · Booked · You can (edge cases) |
| Glance | Middle column | Proof metrics + decisions made |
| Books | Right column | Snapshot + trial balance |
| Matches | Bottom row LTR | Sales pane \| Purchase pane |
| Footer | Bottom | Agent paths only |

**Contract:** primary reading order is **left → right**. Columns scroll internally if needed; do not stack sections into a vertical report.

### Visual system (consistency)

- **Black & white only** — ink on white, grey secondary, no colour chrome  
- **Print-friendly** — offline, single file, inline CSS  
- **Board LTR** — three main columns + bottom dual pane  
- **Typography** — Helvetica/Arial; tabular numbers  
- **No dark theme**

### Action checklist rules

Every open item **must** include:

| Field | Purpose |
|---|---|
| **Title** | Plain language problem |
| **Priority** | `Needs you` · `Optional` · `Info` · `Done` |
| **Why it matters** | One short paragraph |
| **What we booked** | Interim treatment already on the TB |
| **What you can do** | 2–4 concrete actions + **edge case** line where relevant |

**Forbidden:** checklist that only says “see queries.md” or “please confirm.”

Derive items automatically from state + variances, or supply  
`workpapers/action_items.json` as `{ "items": [ ... ] }` for full control.

## When to generate

```bash
python3 scripts/generate_html_report.py clients/<slug>
```

Refresh after TB roll, recon, user answers, or handoff.

## Rules

1. Amounts only from JSON — never retype from memory.  
2. Same section order every time.  
3. No vendor branding; firm name only if profile present (future).  
4. Owner language by default.  
5. Missing HTML at handoff = generate before claiming present done.

## Anti-patterns

- Dark “app UI” HTML as the client pack  
- Different section order per engagement  
- Open queries as a bare bullet list  
- Two `.md` files as “the deliverable”  
- Invented numbers on the page  

## Version

`html-deliverables` **1.2** — 2026-07-09 (horizontal board LTR — not vertical scroll essay).
