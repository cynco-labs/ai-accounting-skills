<p align="center">
  <img src="https://img.shields.io/badge/v2.0.1-release-0d6efd?style=for-the-badge" alt="version" />
  <img src="https://img.shields.io/badge/Claude%20Code-Plugins-f97316?style=for-the-badge" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Beancount-SoR-111827?style=for-the-badge" alt="Beancount" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-10b981?style=for-the-badge" alt="License" />
</p>

<h1 align="center">AI Accounting Skills</h1>

<p align="center">
  <strong>Agent-native accounting engagements — from a messy folder of banks & receipts<br/>to balanced books, MPERS financials, Beancount ledger, and Fava.</strong>
</p>

<p align="center">
  Drop files. Say “do the year end.” The agent runs a real pipeline — not a vibe.
</p>

<p align="center">
  <a href="#-install-60-seconds"><strong>Install</strong></a> ·
  <a href="#-what-you-get"><strong>What you get</strong></a> ·
  <a href="#-pipeline"><strong>Pipeline</strong></a> ·
  <a href="#-for-agents"><strong>For agents</strong></a> ·
  <a href="./QUICKSTART.md"><strong>Quickstart</strong></a> ·
  <a href="#-disclaimer"><strong>Disclaimer</strong></a>
</p>

---

## Why this exists

Coding agents are great at code — and lost at **where accounting numbers should live**.

| Without this | With this |
|---|---|
| Random Excel, no gates | JSON workpapers → **balanced TB** or stop |
| Invented company context | **Smart intake** — read docs, ask ≤3 questions |
| “Looks fine” books | Bank recon **RM 0.00**, line-balance proof |
| No system of record | **Beancount** ledger + **Fava** UI |
| One opaque prompt | **34 skills**, stage plugins, resume state |

Built for [Claude Code](https://claude.com/product/claude-code) / Cowork as a **plugin marketplace**. Malaysia (MPERS / MFRS / ITA) ships first; other jurisdictions plug in.

---

## ⚡ Install

### A) `npx` CLI (zero clone)

```bash
# Instant demo — golden ledger in Fava
npx @cynco/accounting-skills demo

# Bank PDFs → Excel
npx @cynco/accounting-skills extract ./statements --out ./bank.xlsx

# Client journals → Beancount + Fava
npx @cynco/accounting-skills ledger ./clients/acme --fava

# Scaffold workspace
npx @cynco/accounting-skills init acme-sdn-bhd

# Doctor / CI
npx @cynco/accounting-skills doctor
npx @cynco/accounting-skills check
```

Requires **Python 3** + `pip install -r requirements.txt` (or deps the CLI prints).

### B) Claude Code plugins

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

Restart Claude Code, then:

```text
/accounting-engagement:cold-start-interview   # firm defaults (2–15 min)
```

**Throw work at it:**

> Here are bank statements and receipts in this folder. Do the accounting.

Default skill: `full-engagement-pipeline` → smart intake → extract → books → QC → **Beancount** → optional **Fava**.

Full detail: **[QUICKSTART.md](./QUICKSTART.md)** · CLI: **[cli/README.md](./cli/README.md)**
---

## 📦 What you get

```
┌────────────────────────────────────────────────────────────┐
│  accounting-engagement          one-install umbrella       │
│  12 stage plugins               modular if you prefer      │
│  34 pipeline skills             fat-trigger descriptions   │
│  Smart intake                   infer first, ask last      │
│  Maybank PDF extractor          pdfplumber + balance proof │
│  JSON schemas + validators      machine-checkable books    │
│  Beancount + Fava               ledger SoR + web UI        │
│  MPERS notes + industry COAs    disclosure & overlays      │
│  ci_check.sh                    OSS-grade gates            │
└────────────────────────────────────────────────────────────┘
```

| Layer | Technology | Role |
|:------|:-----------|:-----|
| Intermediate truth | `workpapers/*.json` | What agents verify |
| Human packs | **openpyxl** Excel | Review / client workpapers |
| Ledger SoR | **Beancount** `.beancount` | Final double-entry |
| Interactive UI | **Fava** `localhost:5000` | Browse P&L / BS / journals |

---

## 🔁 Pipeline

```text
  Folder dump
       │
       ▼
  smart-intake  ── infer entity, MYR, period; ≤3 questions
       │
       ▼
  extract banks ── CSV or Maybank PDF script (not vision-first)
       │
       ▼
  classify → journals → bank recon (RM0) → TB
       │
       ▼
  year-end AJEs → ATB → MPERS review → FS + notes
       │
       ▼
  QC (Section A blockers) → finalise
       │
       ├──────────────► Beancount  ── system of record
       │                      │
       │                      └── Fava UI
       └──────────────► tax computation (locked figures)
```

Resume anytime from `engagement_state.json` (SessionStart hook on umbrella).

---

## 🧠 For agents

| Do | Don't |
|---|---|
| Read docs before interrogating | 20-field setup forms |
| Run repo scripts when they exist | Reinvent Maybank parsers in chat |
| Prove bank/TB balance | Invent lines to “make it work” |
| Export Beancount after lock | Treat Excel as the only ledger |
| Write disk artifacts every stage | Rely on chat memory |

Doctrine: [`shared/agent-runtime.md`](./shared/agent-runtime.md) · [`shared/architecture.md`](./shared/architecture.md) · [`shared/guardrails.md`](./shared/guardrails.md)

```bash
pip install -r requirements.txt
bash scripts/ci_check.sh          # marketplace + golden + routing + bean-check
```

---

## 🔌 Plugins

<details>
<summary><strong>Stage plugins (click to expand)</strong></summary>

| Plugin | Job |
|---|---|
| [`accounting-engagement`](./accounting-engagement) | **Umbrella** — install this |
| [`engagement-accounting`](./engagement-accounting) | Cold-start, smart-intake, pipeline |
| [`bookkeeping-accounting`](./bookkeeping-accounting) | Extract, classify, journals |
| [`reconciliation-accounting`](./reconciliation-accounting) | Bank + subledgers + TB |
| [`year-end-accounting`](./year-end-accounting) | YE adjustments + ATB |
| [`mpers-accounting`](./mpers-accounting) | Standards review + disclosures |
| [`financial-statements-accounting`](./financial-statements-accounting) | Primaries, notes, workbook |
| [`quality-review-accounting`](./quality-review-accounting) | QC gates |
| [`finalisation-accounting`](./finalisation-accounting) | Lock, approval, auditor pack |
| [`tax-accounting`](./tax-accounting) | MY tax + capital allowances |
| [`beancount-ledger`](./beancount-ledger) | Export ledger + Fava |
| [`accounting-builder-hub`](./accounting-builder-hub) | Skill QA + jurisdiction scaffold |

</details>

Marketplace id (for `/plugin install`): **`claude-for-accounting`**

---

## 🏦 Bank extract (fast path)

Maybank Islamic e-statements (proven on real multi-month books):

```bash
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank_transactions.xlsx \
  --also-json ./workpapers/transactions.json \
  --fail-on-error
```

Text layer + regex + **Decimal running-balance proof** — not vision-first.  
See [`references/bank_statement_extraction.md`](./references/bank_statement_extraction.md).

---

## 📒 Beancount + Fava

```bash
python3 scripts/export_to_beancount.py \
  --client-dir path/to/client \
  --output path/to/client/ledger/main.beancount \
  --bean-check

scripts/run_fava.sh path/to/client/ledger/main.beancount
# → http://127.0.0.1:5000
```

---

## 🧪 Verify the repo

```bash
git clone https://github.com/cynco-labs/ai-accounting-skills.git
cd ai-accounting-skills
pip install -r requirements.txt
bash scripts/ci_check.sh
```

Golden fixture: `fixtures/golden-mini-sdn-bhd` (synthetic — not a real client).

---

## 🗺 Roadmap (honest)

- [x] Stage plugins + umbrella  
- [x] Smart intake + engagement state  
- [x] Maybank Islamic PDF extractor  
- [x] Beancount SoR + Fava  
- [x] CI / schema / routing evals  
- [ ] More bank PDF adapters  
- [ ] Leaner Beancount opens (used accounts only)  
- [ ] Additional jurisdiction packs  

---

## ⚠️ Disclaimer

**Drafts for professional accountant review only.**

Not signed financial statements. Not an audit or review opinion. Not tax advice.  
Not a substitute for a licensed professional. Not official MASB / MIA / LHDN positions.

The reviewing accountant verifies figures against sources and takes responsibility for anything issued.

---

## 👤 Maintainers & license

**Hazli Johar** — [coding@hazli.dev](mailto:coding@hazli.dev) · [cynco-labs](https://github.com/cynco-labs)

Apache License 2.0 — see [LICENSE](./LICENSE).

Contributions welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md). Run `bash scripts/ci_check.sh` before PRs.

---

<p align="center">
  <sub>Throw a client folder at an agent. Get books you can defend.</sub>
</p>
