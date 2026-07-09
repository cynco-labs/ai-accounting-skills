---
name: prove
description: Prove the job for this engagement depth (books scorecard or full QC).
disable-model-invocation: true
---
# /prove

Prove path is **depth-scoped** — not always a full year-end QC pack.

## Do this

1. Read `engagement_state.json` → `engagement_type` (default `bookkeeping_only`).  
2. Load `shared/runtime-brief.md` · `references/depth_gates.json`.  
3. Branch:

### A — `bookkeeping_only` (default)

1. Run depth scorecard (strict):

```bash
python3 scripts/depth_gates.py <client> --strict
# or: npx @cynco/accounting-skills close <client> --no-export-ledger
```

2. Required: register · transactions · journals · bank recon 0 · prelim TB balances.  
3. Optional: `export-beancount` · `open-fava` if user wants a ledger UI.  
4. On green: set `status: done` for **books only**; say “Books for [period] are ready.”  
5. Do **not** open full `quality-review` / FS unless user upgrades depth.

### B — `year_end` / `compilation` / `year_end_tax`

1. Load **`quality-review`** (`quality-review-accounting/skills/quality-review/SKILL.md`).  
2. Include standards-aware checks when `classify_depth` requires.  
3. Run `depth_gates.py --strict` (or `close`) so ATB + FS + QC Section A pass.  
4. Lock via **`finalise-accounts`** only after user confirms.  
5. Optional after lock: **`export-beancount`** · **`open-fava`**.  
6. Tax only for `year_end_tax`.

**Done when:** depth scorecard green for this `engagement_type`; human message matches depth (books ready vs year-end pack ready).

See `shared/slash-surface.md` · `scripts/depth_gates.py`.
