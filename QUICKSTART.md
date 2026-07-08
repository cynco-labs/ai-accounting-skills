# Quick Start

**skills.sh · Claude plugins · npm CLI — then throw a folder at the agent.**

## 0. Install skills (pick one)

### A) skills.sh — any supported agent

```bash
# See what's in the package (~36 skills)
npx skills add cynco-labs/ai-accounting-skills --list

# Install all skills globally
npx skills add cynco-labs/ai-accounting-skills --all -g

# Or install a few high-value ones
npx skills add cynco-labs/ai-accounting-skills \
  --skill full-engagement-pipeline \
  --skill extract-bank-statement \
  --skill smart-intake \
  --skill export-beancount \
  -g -y
```

Browse: [skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

### B) Claude Code plugin marketplace

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

Restart Claude Code. Prefer **user scope** so the plugin can read client files outside the project folder.

Optional modular list: `bash scripts/install_all.sh`

### C) npm CLI tools (extract / ledger / Fava)

```bash
npx @cynco/accounting-skills demo          # Fava on golden ledger
npx @cynco/accounting-skills doctor        # check Python deps
npx @cynco/accounting-skills extract ./banks --out ./bank.xlsx
```

## 1. Firm cold-start (once, Claude plugins)

```text
/accounting-engagement:cold-start-interview
```

Writes firm defaults under `~/.claude/plugins/config/claude-for-accounting/`.

## 2. Throw work

Point at a folder of bank statements / receipts:

> Do the accounting for whatever is in this folder.

Or (Claude plugins):

```text
/accounting-engagement:full-engagement-pipeline
```

The agent should:

1. **Smart-intake** — read docs, infer MY/MYR/entity/period, ask ≤3 questions  
2. Extract banks (Maybank PDF script or CSV)  
3. Classify → journals → recon → TB → YE → FS → QC  
4. Finalise → **Beancount** → optional **Fava**

## 3. Scripts (local machine)

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

## 4. Verify this repo

```bash
bash scripts/ci_check.sh
```
