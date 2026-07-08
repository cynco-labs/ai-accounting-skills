# Agent install recipes

Same skills package. Different shells.

| Agent | Recipe |
|:------|:-------|
| [Claude Code](./claude-code.md) | skills.sh **or** plugin marketplace |
| [Codex](./codex.md) | skills.sh → `.agents/skills/` |
| [Cursor](./cursor.md) | skills.sh → `.agents/skills/` / `~/.cursor/skills/` |
| [Grok / xAI](./grok-xai.md) | skills.sh + CLI tools |
| [GLM](./glm.md) | skills.sh |
| [Kimi](./kimi.md) | skills.sh |

**Universal install**

```bash
npx skills add cynco-labs/ai-accounting-skills
```

**Universal tools (extract / ledger / close / doctor)**

```bash
npx @cynco/accounting-skills doctor
npx @cynco/accounting-skills close fixtures/golden-mini-sdn-bhd
```

**Firm profile (all agents)**

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
# → ~/.config/ai-accounting/firm-profile.md
```

See [`shared/firm-profile.md`](../../shared/firm-profile.md).
