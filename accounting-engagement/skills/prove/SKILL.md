---
name: prove
description: Prove the job for this engagement depth (books scorecard or full QC).
disable-model-invocation: true
---
# /prove

Depth-scoped prove — not always year-end QC.

## Do this

1. Read `engagement_state.json` → `engagement_type` (default `bookkeeping_only`).  
2. Load `shared/runtime-brief.md` · `references/depth_gates.json`.  
3. Refresh HTML pack (required gate):

```bash
python3 scripts/generate_html_report.py <client>
```

4. Branch:

### A — `bookkeeping_only` (default)

```bash
python3 scripts/depth_gates.py <client> --strict
# or: python3 scripts/close_engagement.py <client> --no-export-ledger
```

Required: register · txns · journals · bank recon 0 · prelim TB · **`outputs/*_pack.html`**.  
Optional: Beancount export · Fava (explore only — not the handoff).  
On green: `status: done` · tell user **open the HTML pack path** · “Books for [period] are ready.”  
Do **not** open full QC/FS unless user upgrades depth.

### B — `year_end` / `compilation` / `year_end_tax`

1. **`quality-review`** then `depth_gates.py --strict` (ATB + FS + QC A + HTML).  
2. Lock via **`finalise-accounts`** only after user confirms.  
3. Optional: export Beancount · Fava. Tax only for `year_end_tax`.

**Done when:** `depth_gates --strict` green; user message points at **HTML pack**, not a list of `.md` files.

See `shared/slash-surface.md` · `scripts/depth_gates.py`.
