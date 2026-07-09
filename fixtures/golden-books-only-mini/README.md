# Golden Books-Only Mini — SYNTHETIC FIXTURE

**Not a real client.** Default product path: `engagement_type: bookkeeping_only`.

- Entity: Sdn Bhd / MPERS (sample)
- Period: 2025 (same small numbers as year-end mini for math)
- Purpose: prove **depth-scoped Done** — books stop at prelim TB + recon

## What is intentionally missing

- No YE journals / adjusted TB
- No FS / notes / QC pack
- No tax

## Expected

```bash
python3 scripts/depth_gates.py fixtures/golden-books-only-mini --strict
python3 scripts/close_engagement.py fixtures/golden-books-only-mini --no-export-ledger
```

Both exit 0. Scorecard depth = `bookkeeping_only`.
