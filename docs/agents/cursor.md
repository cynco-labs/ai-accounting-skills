# Cursor

## Install

```bash
npx skills add cynco-labs/ai-accounting-skills -g -a cursor -y
```

Or project-scoped (committed with the repo):

```bash
npx skills add cynco-labs/ai-accounting-skills -a cursor -y
```

## Firm profile

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
```

Project override: `./.ai-accounting/firm-profile.md`.

## Workflow

1. Open the client folder as the Cursor workspace (or monorepo root).  
2. Install skills; ask the agent to run `full-engagement-pipeline` / smart intake.  
3. For deterministic money steps, shell out:

```bash
npx @cynco/accounting-skills extract ./source/bank --out ./outputs/bank.xlsx --json ./workpapers/transactions.json
npx @cynco/accounting-skills classify ./workpapers/transactions.json
npx @cynco/accounting-skills close .
```

## Notes

- Skills are procedural knowledge; **scripts are the system of truth for extracts**.  
- Keep workpapers in-repo for PR review when working as a team.  
