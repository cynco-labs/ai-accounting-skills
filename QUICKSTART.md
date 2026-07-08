# Quick Start

**CLI in one line · plugins in one minute · then throw a folder at the agent.**

## 0. Try the CLI first (optional)

```bash
npx @cynco/accounting-skills demo          # Fava on golden ledger
npx @cynco/accounting-skills doctor        # check Python deps
npx @cynco/accounting-skills extract ./banks --out ./bank.xlsx
```

## 1. Install marketplace + umbrella

In **Claude Code**:

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

Restart Claude Code.

> Prefer **user scope** so the plugin can read client files outside the project folder.

Optional modular install list: `bash scripts/install_all.sh`

## 2. Firm cold-start (once)

```text
/accounting-engagement:cold-start-interview
```

Writes firm defaults under `~/.claude/plugins/config/claude-for-accounting/`.

## 3. Throw work

Point at a folder of bank statements / receipts:

> Do the accounting for whatever is in this folder.

Or:

```text
/accounting-engagement:full-engagement-pipeline
```

The agent should:

1. **Smart-intake** — read docs, infer MY/MYR/entity/period, ask ≤3 questions  
2. Extract banks (Maybank PDF script or CSV)  
3. Classify → journals → recon → TB → YE → FS → QC  
4. Finalise → **Beancount** → optional **Fava**

## 4. Scripts (local machine)

```bash
git clone https://github.com/cynco-labs/ai-accounting-skills.git
cd ai-accounting-skills
pip install -r requirements.txt

# Maybank Islamic PDFs → Excel + JSON
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank.xlsx \
  --also-json ./transactions.json \
  --fail-on-error

# Final journals → Beancount SoR + Fava
python3 scripts/export_to_beancount.py \
  --client-dir /path/to/client \
  --output /path/to/client/ledger/main.beancount \
  --bean-check
scripts/run_fava.sh /path/to/client/ledger/main.beancount
```

## 5. Verify this repo

```bash
bash scripts/ci_check.sh
```

## Stuck?

| Symptom | Fix |
|---|---|
| Command not found | Restart Claude Code after install |
| Generic / provisional output | Run cold-start interview |
| Balance / bank fails | Treat as blocker — fix sources, don’t invent lines |
| No Fava | `pip install beancount fava` |

Full reference: [README.md](./README.md)
