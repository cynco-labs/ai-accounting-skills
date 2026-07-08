# Claude Code

## Install skills

### Option A — skills.sh (recommended multi-agent path)

```bash
npx skills add cynco-labs/ai-accounting-skills --all -g -a claude-code -y
```

Skills land under `~/.claude/skills/`.

### Option B — Plugin marketplace (umbrella + hooks)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

Then:

```text
/accounting-engagement:cold-start-interview
```

## Firm profile

Preferred:

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
```

Legacy (still read):

```text
~/.claude/plugins/config/claude-for-accounting/firm-profile.md
```

## Throw work

> Here are bank statements in this folder. Do the accounting.

Entry skills: `full-engagement-pipeline` · `smart-intake`.

## Claude-only extras

| Feature | Notes |
|---|---|
| SessionStart resume hook | Umbrella plugin only |
| `/plugin` slash skills | Marketplace install |
| Plugin `CLAUDE.md` overlays | Under plugin config dir |

CLI tools work the same as every other agent:

```bash
npx @cynco/accounting-skills extract ./statements --out ./bank.xlsx
npx @cynco/accounting-skills close ./clients/acme
```
