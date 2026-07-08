# Kimi

## Install

```bash
npx skills add cynco-labs/ai-accounting-skills --all -g -y
```

If Kimi’s agent id is supported by `npx skills`, pass `-a <id>`. Otherwise install globally and ensure Kimi loads skills from the standard directory.

## Recommended loop

```bash
npx @cynco/accounting-skills init client-slug
# drop PDFs/CSVs into clients/client-slug/source/bank/
npx @cynco/accounting-skills extract ./clients/client-slug/source/bank \
  --out ./clients/client-slug/outputs/bank.xlsx \
  --json ./clients/client-slug/workpapers/transactions.json
npx @cynco/accounting-skills classify ./clients/client-slug/workpapers/transactions.json
# continue books via skills (journals → recon → TB → YE → FS → QC)
npx @cynco/accounting-skills close ./clients/client-slug
npx @cynco/accounting-skills ledger ./clients/client-slug --fava
```

## Firm profile

```bash
python3 scripts/resolve_firm_profile.py --init "Your Firm"
```

## Guardrails

Never fabricate numbers. Re-read source documents after context loss.  
Bank recon and trial balance must hit **RM 0.00** difference.
