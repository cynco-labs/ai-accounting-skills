# GLM

## Install

```bash
npx skills add cynco-labs/ai-accounting-skills --all -g -y
```

Use the agent flag your GLM coding CLI registers with the skills tool (if listed). Otherwise global install + manual skills path is fine.

## CLI backbone

```bash
npx @cynco/accounting-skills demo
npx @cynco/accounting-skills extract ./banks --out ./bank.xlsx
npx @cynco/accounting-skills classify ./workpapers/transactions.json
npx @cynco/accounting-skills close ./clients/acme
```

## Firm profile

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
```

## Practice notes

- Malaysia-first pack (MPERS / MYR).  
- Prefer CSV bank exports when PDF adapters are missing.  
- Classifier proposes codes; humans confirm low-confidence rows (`needs_review`).  
