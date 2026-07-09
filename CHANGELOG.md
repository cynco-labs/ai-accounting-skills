# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project versioning follows [SemVer](https://semver.org/) for plugin contracts.

## [2.2.2] — 2026-07-09

### Changed

- **Period-first doctrine** — agents book whatever months are on disk deeply; do not pressure users for 12 months to start
- Full-year FS is an opt-in upgrade when coverage supports it; partial coverage = AMBER on YE claims only
- Soft-confirm examples and smart-intake defaults → `bookkeeping_only` for period-on-disk

## [2.2.1] — 2026-07-09

### Added

- **`shared/user-questions.md`** — progress-gating asks must use host structured question tools (`ask_user_question` / `AskUserQuestion`); fallback letter protocol when no tool

### Changed

- `smart-intake`, `full-engagement-pipeline`, `classify-transactions`, `resume-engagement` require structured asks
- `agent-runtime`, `guardrails`, `skill-design-framework`, agent recipes (Grok / Claude) document the rule

## [2.2.0] — 2026-07-09

### Added

- **Kernel contract** — `shared/kernel-contract.md` (truth shapes + pure functions)
- **Skill collapse map** — `shared/skill-collapse-map.md` (36 → 6 intents, frozen renames)
- **`post_journals.py` / CLI `post`** — classified transactions → balancing journals
- **`roll_tb.py` / CLI `tb`** — journals → trial balance (preliminary / adjusted); agents must not freestyle TB
- CI: golden TB must match `roll_tb --check`
- Unit tests for post + roll_tb

### Changed

- `preliminary-trial-balance` / `adjusted-trial-balance` skills are **engine-only** (doctrine deleted)
- `journal-entries` requires `post_journals.py` then `roll_tb`
- `full-engagement-pipeline` loads kernel contract; TB stages call `roll_tb.py`
- `close --roll-tb` re-derives TB before prove

## [2.1.0] — 2026-07-09

### Added

- **`close`** — end-to-end engagement proof (validate · stage gates · Beancount summary)
- **`classify`** — deterministic COA classification + review queue (`scripts/classify_transactions.py`)
- **`extract_bank.py`** — unified adapter router (Maybank PDF · CIMB CSV · generic CSV)
- **`firm`** — multi-agent firm profile resolution (`~/.config/ai-accounting/`)
- Stage gates validator · unit test suite · agent recipes under `docs/agents/`
- `references/classification_patterns.json` (Malaysia pattern pack)

### Changed

- CLI help is multi-agent (skills.sh first; Claude plugins optional)
- `ci_check.sh` runs unittest + stage gates + close proof
- Classify / extract skills require scripts before chat freestyle

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
