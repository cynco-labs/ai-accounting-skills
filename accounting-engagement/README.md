# accounting-engagement (umbrella)

**One install** for agents and humans who will throw a client folder at Claude and say “do the year end.”

## Install

```text
/plugin marketplace add <path-or-url-to-claude-for-accounting>
/plugin install accounting-engagement@claude-for-accounting
```

Restart Claude Code. Optional firm setup:

```text
/accounting-engagement:cold-start-interview
```

## What you get

- All stage skills (synced from modular plugins — source of truth stays modular)
- `full-engagement-pipeline` as DEFAULT throw-work entry
- `resume-engagement` + SessionStart hook when `engagement_state.json` is nearby
- Same guardrails and artifact contracts as the monorepo

## Maintainers

Do **not** edit `skills/*/SKILL.md` in this plugin by hand.

```bash
python3 scripts/sync_umbrella.py
python3 scripts/sync_umbrella.py --check   # CI
```

## Modular alternative

Install stage plugins individually — see `scripts/install_all.sh`.
