<p align="center">
  <img src="https://img.shields.io/badge/v2.0.1-0d6efd?style=for-the-badge" alt="v2.0.1" />
  <a href="https://skills.sh/cynco-labs/ai-accounting-skills"><img src="https://skills.sh/b/cynco-labs/ai-accounting-skills" alt="skills.sh" /></a>
  <img src="https://img.shields.io/badge/Beancount-SoR-111827?style=for-the-badge" alt="Beancount" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-10b981?style=for-the-badge" alt="License" />
</p>

<h1 align="center">AI Accounting Skills</h1>

<p align="center">
  <strong>Folder dump → balanced books → MPERS financials → Beancount + Fava.</strong><br/>
  Agent-native accounting for the tools teams actually use.
</p>

<p align="center">
  Drop bank statements & receipts. Say <em>“do the year end.”</em><br/>
  The agent runs a real pipeline — gates, proofs, and artifacts on disk.
</p>

---

## Works with your agent

Install once via [skills.sh](https://skills.sh/cynco-labs/ai-accounting-skills) — same `SKILL.md` package across the major coding agents.

<p align="center">
  <a href="https://claude.com/product/claude-code"><img src="https://www.skills.sh/agents/claude-code.svg" height="44" alt="Claude Code" /></a>&nbsp;&nbsp;
  <a href="https://openai.com/codex"><img src="https://www.skills.sh/agents/codex.svg" height="44" alt="Codex" /></a>&nbsp;&nbsp;
  <a href="https://cursor.com"><img src="https://www.skills.sh/agents/cursor.svg" height="44" alt="Cursor" /></a>&nbsp;&nbsp;
  <a href="https://x.ai"><img src="https://img.shields.io/badge/Grok%20%2F%20xAI-000000?style=for-the-badge&logo=x&logoColor=white" alt="Grok / xAI" height="44" /></a>&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/GLM-1a56db?style=for-the-badge" alt="GLM" height="44" />&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Kimi-6d28d9?style=for-the-badge" alt="Kimi" height="44" />
</p>

<p align="center">
  <sub>
    <b>Claude Code</b> · <b>Codex</b> · <b>Cursor</b> · <b>Grok / xAI</b> · <b>GLM</b> · <b>Kimi</b>
    &nbsp;·&nbsp; + OpenCode, Windsurf, Copilot, Gemini CLI, and <a href="https://github.com/vercel-labs/skills#supported-agents">40+ more</a>
  </sub>
</p>

| Agent | How to load skills |
|:------|:-------------------|
| **All of the above** (recommended) | `npx skills add cynco-labs/ai-accounting-skills` |
| **Claude Code** (full plugin marketplace) | `/plugin marketplace add` + install umbrella (below) |
| **Any terminal** (extract / ledger / Fava) | `npx @cynco/accounting-skills …` |

Malaysia (MPERS / MFRS / ITA) ships first. Other jurisdictions plug in via the builder hub.

---

## Install

### 1 · Skills — any agent

```bash
npx skills add cynco-labs/ai-accounting-skills
```

```bash
# List · install all · pick a few
npx skills add cynco-labs/ai-accounting-skills --list
npx skills add cynco-labs/ai-accounting-skills --all -g
npx skills add cynco-labs/ai-accounting-skills \
  --skill full-engagement-pipeline \
  --skill extract-bank-statement \
  --skill smart-intake -g -y
```

→ [skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

### 2 · Claude Code plugins (optional, full umbrella)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

```text
/accounting-engagement:cold-start-interview
```

Then:

> Here are bank statements and receipts in this folder. Do the accounting.

---

## CLI · `npx`

Zero clone. Scripts that agents and humans both run.

```bash
npx @cynco/accounting-skills <command>
```

| Command | What you get |
|:--------|:-------------|
| `demo` | Golden mini ledger → **Fava** in the browser |
| `extract ./statements` | Bank PDF/CSV → Excel (+ JSON) |
| `ledger ./clients/acme --fava` | Journals → Beancount + Fava |
| `init acme-sdn-bhd` | Client workspace scaffold |
| `doctor` | Python / deps health check |
| `check` | Validate engagement or full CI |

```bash
npx @cynco/accounting-skills demo
npx @cynco/accounting-skills extract ./statements --out ./bank.xlsx
npx @cynco/accounting-skills ledger ./clients/acme --fava
npx @cynco/accounting-skills doctor
```

Needs **Node ≥ 18** + **Python 3**. Install deps with `pip install -r requirements.txt` (or whatever `doctor` prints).

<details>
<summary><strong>More CLI detail</strong></summary>

- Package: [`@cynco/accounting-skills`](https://www.npmjs.com/package/@cynco/accounting-skills)
- Docs: [cli/README.md](./cli/README.md) · [QUICKSTART.md](./QUICKSTART.md)
- From a local clone: `node cli/bin/ai-accounting.js doctor`

</details>

---

## Why this exists

Coding agents ship code. They usually invent accounting.

| Without this | With this |
|---|---|
| Random Excel, no gates | JSON workpapers → **balanced TB** or stop |
| Invented company context | **Smart intake** — read docs, ask ≤3 questions |
| “Looks fine” books | Bank recon **RM 0.00**, line-balance proof |
| No system of record | **Beancount** ledger + **Fava** UI |
| One opaque prompt | **36 skills**, stage plugins, resume state |

---

## What you get

```
┌────────────────────────────────────────────────────────────┐
│  36 pipeline skills          fat-trigger, multi-agent      │
│  skills.sh + Claude plugins  install path for every stack  │
│  Smart intake                infer first, ask last         │
│  Maybank PDF extractor       pdfplumber + balance proof    │
│  JSON schemas + validators   machine-checkable books       │
│  Beancount + Fava            ledger SoR + web UI           │
│  MPERS notes + industry COAs disclosure & overlays         │
│  npm CLI                     extract · ledger · doctor     │
│  ci_check.sh                 OSS-grade gates               │
└────────────────────────────────────────────────────────────┘
```

| Layer | Technology | Role |
|:------|:-----------|:-----|
| Intermediate truth | `workpapers/*.json` | What agents verify |
| Human packs | **openpyxl** Excel | Review / client workpapers |
| Ledger SoR | **Beancount** `.beancount` | Final double-entry |
| Interactive UI | **Fava** `localhost:5000` | Browse P&L / BS / journals |

---

## Pipeline

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

Resume anytime from `engagement_state.json`.

---

## For agents

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
bash scripts/ci_check.sh
```

---

## Plugins (Claude marketplace)

<details>
<summary><strong>Stage plugins</strong></summary>

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

Marketplace id: **`claude-for-accounting`**

</details>

---

## Bank extract

Maybank Islamic e-statements (proven on real multi-month books):

```bash
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank_transactions.xlsx \
  --also-json ./workpapers/transactions.json \
  --fail-on-error
```

Text layer + regex + **Decimal running-balance proof** — not vision-first.  
[`references/bank_statement_extraction.md`](./references/bank_statement_extraction.md)

---

## Beancount + Fava

```bash
python3 scripts/export_to_beancount.py \
  --client-dir path/to/client \
  --output path/to/client/ledger/main.beancount \
  --bean-check

scripts/run_fava.sh path/to/client/ledger/main.beancount
# → http://127.0.0.1:5000
```

---

## Verify

```bash
git clone https://github.com/cynco-labs/ai-accounting-skills.git
cd ai-accounting-skills
pip install -r requirements.txt
bash scripts/ci_check.sh
```

Golden fixture: `fixtures/golden-mini-sdn-bhd` (synthetic — not a real client).

---

## Roadmap

### Shipped

- [x] Full engagement pipeline (intake → books → QC → lock)
- [x] Stage plugins + umbrella (`accounting-engagement`)
- [x] Smart intake + `engagement_state` resume
- [x] Maybank Islamic PDF extractor (balance-proof)
- [x] Beancount system of record + Fava UI
- [x] JSON schemas, validators, routing evals, `ci_check.sh`
- [x] npm CLI `@cynco/accounting-skills` (`demo` · `extract` · `ledger` · `doctor`)
- [x] [skills.sh](https://skills.sh/cynco-labs/ai-accounting-skills) multi-agent install
- [x] Claude Code marketplace (`claude-for-accounting`)
- [x] MPERS notes templates + industry COA overlays
- [x] Golden fixture + OSS docs (Apache 2.0)

### Near term

- [ ] More bank PDF adapters (CIMB, Public Bank, HSBC, RHB, …)
- [ ] Leaner Beancount opens (used accounts only)
- [ ] One-command “engagement demo” from empty folder → Fava
- [ ] Skills telemetry / install badges per skill
- [ ] Agent install recipes (Cursor · Codex · Grok · GLM · Kimi)

### Next

- [ ] Additional jurisdiction packs (SG · UK · AU · US)
- [ ] AR/AP subledger deep skills + aging packs
- [ ] Fixed-asset register → depreciation → CA schedule end-to-end
- [ ] SST / GST / e-Invoice (MY) assist skills
- [ ] Multi-entity / group consolidation skeleton
- [ ] Diff-friendly workpaper formats for PR review

### Later

- [ ] Connector pack (bank CSV drop folders, cloud drive intake)
- [ ] Managed-agent cookbooks (deadline watcher, monthly close)
- [ ] Eval harness: extract accuracy + TB balance on golden sets
- [ ] Signed release attestations for skill packages
- [ ] Community skill extensions without forking the core pipeline

---

## Disclaimer

**Drafts for professional accountant review only.**

Not signed financial statements. Not an audit or review opinion. Not tax advice.  
Not a substitute for a licensed professional. Not official MASB / MIA / LHDN positions.

The reviewing accountant verifies figures against sources and takes responsibility for anything issued.

---

## Maintainers & license

**Hazli Johar** — [coding@hazli.dev](mailto:coding@hazli.dev) · [cynco-labs](https://github.com/cynco-labs)

Apache License 2.0 — [LICENSE](./LICENSE) · Contributions — [CONTRIBUTING.md](./CONTRIBUTING.md)

```bash
bash scripts/ci_check.sh   # before PRs
```

---

<p align="center">
  <sub>
    <a href="https://skills.sh/cynco-labs/ai-accounting-skills">skills.sh</a> ·
    <a href="https://www.npmjs.com/package/@cynco/accounting-skills">npm</a> ·
    <a href="https://github.com/cynco-labs/ai-accounting-skills">GitHub</a>
  </sub><br/>
  <sub>Throw a client folder at any agent. Get books you can defend.</sub>
</p>
