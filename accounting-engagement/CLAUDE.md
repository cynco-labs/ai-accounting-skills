<!--
CONFIGURATION

  ~/.claude/plugins/config/claude-for-accounting/accounting-engagement/CLAUDE.md

Prefer firm profile at:
  ~/.claude/plugins/config/claude-for-accounting/firm-profile.md

This file is a TEMPLATE.
-->

# Accounting Engagement (Umbrella) Profile

**Mode:** throw-work agent (default full-engagement-pipeline)
**Jurisdiction pack:** [PLACEHOLDER]
**Active client path:** [PLACEHOLDER]

## Agent defaults

- DEFAULT entry skill: `full-engagement-pipeline`
- Resume skill: `resume-engagement`
- Disk is truth: `engagement_state.json` + stage artifacts
- Validate: `python3 scripts/validate_engagement_artifacts.py <client>`
