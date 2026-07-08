# Grok / xAI

## Install

Agent Skills are open format. Install via the skills CLI into whatever skill directory your Grok/xAI coding surface supports:

```bash
npx skills add cynco-labs/ai-accounting-skills --all -g -y
```

If your environment does not auto-detect an agent id, install with `--agent '*'` or copy `SKILL.md` trees into the agent’s skills path.

## Always available: CLI

Grok is excellent at orchestration. Point it at **executable** tools:

```bash
npx @cynco/accounting-skills doctor
npx @cynco/accounting-skills extract ./statements --out ./bank.xlsx --json ./txns.json
npx @cynco/accounting-skills classify ./txns.json
npx @cynco/accounting-skills close ./clients/acme
npx @cynco/accounting-skills ledger ./clients/acme --fava
```

## Firm profile

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
export AI_ACCOUNTING_CONFIG="$HOME/.config/ai-accounting"
```

## Doctrine for Grok

| Do | Don't |
|---|---|
| Run extract/classify scripts | Vision-parse 1000 PDF lines in chat |
| Prove bank RM0 and TB balance | Invent missing months |
| Write `workpapers/*.json` | Keep the only copy of numbers in chat |

Repo doctrine: [`shared/guardrails.md`](../../shared/guardrails.md) · [`shared/agent-runtime.md`](../../shared/agent-runtime.md)
