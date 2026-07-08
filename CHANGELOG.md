# Changelog

All notable changes to this project are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Project versioning follows [SemVer](https://semver.org/) for plugin contracts.

## [1.1.0] — 2026-07-09

### Added

- Open-source project framing aligned with claude-for-legal patterns
- Apache License 2.0, CONTRIBUTING, CODE_OF_CONDUCT, CLA, SECURITY, MAINTAINERS
- `shared/skill-design-framework.md` and `shared/jurisdiction-extension-guide.md`
- `scripts/validate_marketplace.py` + GitHub Actions workflow
- `accounting-builder-hub` plugin (`skills-qa`, `jurisdiction-scaffold`, cold-start)
- MPERS notes templates under `references/notes-templates/mpers/`
- Industry COA overlays under `references/coa_templates/industry/`
- Jurisdiction layout `references/jurisdictions/malaysia/`
- CONNECTORS.md and managed-agent cookbooks (filing deadlines, bank intake)
- Pipeline reference and year-end adjustments checklist

### Changed

- Marketplace id / config namespace: `claude-for-accounting`
- White-label firm placeholders (no hard-coded firm identity in templates)
- Plugin versions bumped to 1.1.0

### Notes

- Malaysia remains the first full jurisdiction pack; other packs are extension points

## [1.0.0] — 2026-07-09

### Added

- Initial nine stage plugins and 28 skills covering the engagement pipeline
- Shared guardrails, firm profile template, COA entity templates
- Workbook and PDF generator scripts ported from legacy workflow skill
