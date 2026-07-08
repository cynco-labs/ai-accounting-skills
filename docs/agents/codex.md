# Codex (OpenAI)

## Install

```bash
npx skills add cynco-labs/ai-accounting-skills -g -a codex -y
# or project-local:
npx skills add cynco-labs/ai-accounting-skills -a codex -y
```

Skills install into Codex’s agents skills directory (see [vercel-labs/skills supported agents](https://github.com/vercel-labs/skills#supported-agents)).

## Firm profile

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
```

Reads `~/.config/ai-accounting/firm-profile.md` (not Claude-only paths).

## Workflow

1. Drop banks into a client folder (`npx @cynco/accounting-skills init acme`).  
2. `npx @cynco/accounting-skills extract ./clients/acme/source/bank --json ./clients/acme/workpapers/transactions.json`  
3. `npx @cynco/accounting-skills classify ./clients/acme/workpapers/transactions.json`  
4. Let Codex skills drive journals → TB → YE → FS using disk artifacts.  
5. `npx @cynco/accounting-skills close ./clients/acme --fava`  

## Notes

- No Claude `/plugin` marketplace — use skills.sh.  
- Prefer scripts over re-implementing extract/classify in chat.  
