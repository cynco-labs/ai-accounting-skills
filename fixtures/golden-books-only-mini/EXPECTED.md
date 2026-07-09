# Expected — golden-books-only-mini

```bash
python3 scripts/depth_gates.py fixtures/golden-books-only-mini --strict
python3 scripts/validate_stage_gates.py fixtures/golden-books-only-mini
python3 scripts/close_engagement.py fixtures/golden-books-only-mini --no-export-ledger
```

Must exit 0.

Must **not** require `tb_adjusted.json`, `journals_ye.json`, or `qc_report.md`.

Agent should report: books ready for period; year-end pack not in scope.
