# Quick Start

**Any major agent · one install · throw a folder at it.**

Works with **Claude Code · Codex · Cursor · Grok/xAI · GLM · Kimi** and [40+ agents](https://github.com/vercel-labs/skills#supported-agents) via skills.sh.

---

## 1 · Skills (recommended)

```bash
npx skills add cynco-labs/ai-accounting-skills
```

```bash
npx skills add cynco-labs/ai-accounting-skills --list
npx skills add cynco-labs/ai-accounting-skills --all -g
npx skills add cynco-labs/ai-accounting-skills \
  --skill full-engagement-pipeline \
  --skill extract-bank-statement \
  --skill smart-intake \
  --skill export-beancount \
  -g -y
```

[skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

---

## 2 · CLI tools

```bash
npx @cynco/accounting-skills demo
npx @cynco/accounting-skills doctor
npx @cynco/accounting-skills extract ./banks --out ./bank.xlsx
npx @cynco/accounting-skills ledger ./clients/acme --fava
```

| Command | Result |
|:--------|:-------|
| `demo` | Golden ledger in Fava |
| `extract` | PDF/CSV → Excel |
| `ledger` | Journals → Beancount (+ Fava) |
| `doctor` | Deps check |
| `check` | Validate / CI |

---

## 3 · Claude Code plugins (optional)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

```text
/accounting-engagement:cold-start-interview
```

Prefer **user scope** so the agent can read client files outside the project.

---

## 4 · Throw work

> Do the accounting for whatever is in this folder.

Pipeline: **smart-intake → extract → classify → recon → TB → YE → FS → QC → Beancount → Fava**

---

## 5 · Local scripts

```bash
git clone https://github.com/cynco-labs/ai-accounting-skills.git
cd ai-accounting-skills
pip install -r requirements.txt

python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank.xlsx \
  --also-json ./transactions.json \
  --fail-on-error

python3 scripts/export_to_beancount.py \
  --client-dir /path/to/client \
  --output /path/to/client/ledger/main.beancount \
  --bean-check

scripts/run_fava.sh /path/to/client/ledger/main.beancount
bash scripts/ci_check.sh
```
