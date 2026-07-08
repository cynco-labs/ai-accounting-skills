# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project versioning follows [SemVer](https://semver.org/) for plugin contracts.

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
- **Maybank Islamic PDF extractor:** `scripts/extract_maybank_islamic_pdf.py` + `references/bank_statement_extraction.md`; `extract-bank-statement` skill encodes proven text/regex/balance-proof method (not vision-first)

### Maintainer

- Hazli Johar &lt;coding@hazli.dev&gt;
