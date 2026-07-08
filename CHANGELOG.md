# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project versioning follows [SemVer](https://semver.org/) for plugin contracts.

## [2.0.1] — 2026-07-09

### Fixed

- **`npx @cynco/accounting-skills <cmd>`** failed with `sh: ai-accounting: command not found` because multi-bin packages need a bin matching the unscoped package name (`accounting-skills`). Added that entry (kept `ai-accounting` / `cynco-accounting` aliases).

## [2.0.0] — 2026-07-09

### Changed

- npm package identity: **`@cynco/accounting-skills@2.0.0`** (continues the existing npm name; major bump for full marketplace + CLI + Beancount)
- CLI: `npx @cynco/accounting-skills` (`demo`, `init`, `extract`, `ledger`, `fava`, `check`, `doctor`)
- Primary GitHub home: https://github.com/cynco-labs/ai-accounting-skills

### Notes

- Previous npm `1.0.x` pointed at the older skill-only package; v2 is the agent-native pipeline.
- Claude Code marketplace id remains `claude-for-accounting` for `/plugin install`.
- **2.0.0 is live on npm** (published 2026-07-08). Use **2.0.1+** for reliable bare `npx`.

## [0.0.1] — 2026-07-09

Initial public scaffold of **claude-for-accounting**.

### Added

- Stage plugins for the full engagement pipeline (source documents → bookkeeping → reconciliations → year-end → standards review → financial statements → QC → finalisation → tax)
- `accounting-builder-hub` (skills-qa, jurisdiction-scaffold)
- Shared guardrails, skill design framework, jurisdiction extension guide
- Malaysia jurisdiction pack (MPERS/MFRS, tax, entity types, statutory deductions)
- MPERS notes templates (`references/notes-templates/mpers/`)
- Industry COA overlays (trading, services, F&B, property, construction)
- Managed-agent cookbooks (filing deadline watcher, bank statement intake)
- `scripts/validate_marketplace.py` + GitHub Actions validate workflow
- Apache License 2.0, CONTRIBUTING, CODE_OF_CONDUCT, CLA, SECURITY, MAINTAINERS
- **Agent-native runtime:** `shared/agent-runtime.md`, `engagement_state` schema, stage artifact contracts, fat-trigger skill descriptions, `full-engagement-pipeline` as DEFAULT throw-work entry
- **Umbrella plugin** `accounting-engagement` + `scripts/sync_umbrella.py` + `scripts/install_all.sh`
- **Schemas:** transactions / journals / trial balance + `validate_engagement_artifacts.py`
- **Golden fixture:** `fixtures/golden-mini-sdn-bhd`
- **SessionStart resume hook** + `resume-engagement` skill
- **Utterance routing evals:** `evals/utterance_routing.json` + `eval_utterance_routing.py`
- **Bank extraction:** `extract-bank-statement` skill + `normalize_bank_csv.py`
- **Smart intake:** document-first client discovery (`smart-intake`, `shared/smart-intake.md`) — infer from banks/receipts, ≤3 high-leverage questions, no interrogation theatre
- **Beancount + Fava:** `beancount-ledger` plugin, `export_to_beancount.py`, `run_fava.sh`; ledger SoR after finalisation; Fava UI
- **Production OSS polish:** `requirements.txt`, `scripts/ci_check.sh`, `shared/architecture.md`, `shared/excel_deliverables.md`, tightened CONTRIBUTING/QUICKSTART/CI
- **CLI:** `npx @cynco/accounting-skills` — `demo`, `init`, `extract`, `ledger`, `fava`, `check`, `doctor`
- **Maybank Islamic PDF extractor:** `scripts/extract_maybank_islamic_pdf.py` + `references/bank_statement_extraction.md`; `extract-bank-statement` skill encodes proven text/regex/balance-proof method (not vision-first)

### Maintainer

- Hazli Johar &lt;coding@hazli.dev&gt;
