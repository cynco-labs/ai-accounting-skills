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

Then use the **short slash surface** (recommended):

```text
/accounting-engagement:ask-accounting
/accounting-engagement:do-books
/accounting-engagement:extract
/accounting-engagement:classify
/accounting-engagement:post
/accounting-engagement:present
/accounting-engagement:prove
/accounting-engagement:resume
/accounting-engagement:revenue
/accounting-engagement:capex
```

Firm setup (first install only):

```text
/accounting-engagement:cold-start-interview
```

With **skills.sh** flat install, the same names are often bare: `/do-books`, `/classify`, …

Design: [`shared/slash-surface.md`](../../shared/slash-surface.md).

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

Entry: type `/do-books` (or say “do the accounting”).  
Canonical body: `full-engagement-pipeline` · intake: `smart-intake`.

## Structured questions (mandatory when asking)

Progress-gating asks (entity, period, deliverable, material classification) must use Claude’s **AskUserQuestion** (or equivalent) tool — not chat-only bullets.

Doctrine: [`shared/user-questions.md`](../../shared/user-questions.md).

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
