<p align="center">
  <img src="https://img.shields.io/badge/v2.2.0-0d6efd?style=for-the-badge" alt="v2.2.0" />
  <a href="https://skills.sh/cynco-labs/ai-accounting-skills"><img src="https://skills.sh/b/cynco-labs/ai-accounting-skills" alt="skills.sh" /></a>
  <img src="https://img.shields.io/badge/Beancount-SoR-111827?style=for-the-badge" alt="Beancount" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-10b981?style=for-the-badge" alt="License" />
</p>

<h1 align="center">AI Accounting Skills</h1>

<p align="center">
  <strong>Real accounting for coding agents — not vibe books.</strong><br/>
  Folder dump → balanced books → financials → Beancount + Fava.
</p>

<p align="center">
  Drop bank statements and receipts. Say <em>“do the year end.”</em><br/>
  The agent runs a pipeline with gates, proofs, and artifacts on disk.
</p>

---

## Quickstart (30 seconds)

1. Install:

```bash
npx skills add cynco-labs/ai-accounting-skills
```

2. Point your agent at a folder of banks / receipts and say:

> Do the accounting.

3. Optional — deterministic CLI (no clone):

```bash
npx @cynco/accounting-skills extract ./statements --json ./txns.json
npx @cynco/accounting-skills classify ./txns.json
npx @cynco/accounting-skills post ./clients/acme --opening-from-bank
npx @cynco/accounting-skills tb ./clients/acme --both
npx @cynco/accounting-skills close ./clients/acme
```

That’s it. Resume anytime from `engagement_state.json`.

---

## Why these skills exist

Coding agents ship code fine. They usually invent accounting.

These skills fix the failure modes we see when an agent “does the books” without a real engagement process.

### #1: The agent invents the company

**Problem.** You dump a folder. The agent opens a 20-field questionnaire, or invents the entity name, FY, and framework.

**Fix — smart intake.** Read the documents first. Infer what you can. Soft-confirm entity + period. Ask at most **3** high-leverage questions (structured tool when available). Start extracting banks in the same session.

→ `smart-intake` · `full-engagement-pipeline`

### #2: The numbers don’t prove out

**Problem.** Pretty Excel. TB doesn’t balance. Bank GL doesn’t match the statement. Nobody can defend the pack.

**Fix — kernel + gates.** Extract, classify, post, and **roll_tb** are scripts. Trial balances are **derived only** — never freestyled. Bank recon is **RM 0.00** or an explicit AMBER limitation. QC Section A is a hard blocker before finalisation.

→ `extract` · `classify` · `post` · `roll_tb` · `quality-review`

### #3: Chat is the books

**Problem.** Context compacts. The agent reconstructs figures from memory. Balances drift. Trust dies.

**Fix — disk is truth.** Every stage writes artifacts (`transactions.json`, journals, TB, recon, FS). State lives in `engagement_state.json`. Agents re-read sources after compaction.

→ [`shared/kernel-contract.md`](./shared/kernel-contract.md) · [`CONTEXT.md`](./CONTEXT.md)

### #4: One opaque mega-prompt

**Problem.** A single “do accounts” prompt is unmaintainable. You can’t resume, review, or replace one stage.

**Fix — composable skills.** Six intents (**do-books · extract · classify · post · present · prove**). Stage plugins. One stage at a time. Builder tools stay user-invoked so they never hijack an engagement.

→ [`shared/skill-collapse-map.md`](./shared/skill-collapse-map.md) · [`shared/skill-craft.md`](./shared/skill-craft.md)

### Summary

| Without this | With this |
|---|---|
| Random Excel, no gates | JSON workpapers → **balanced TB** or stop |
| Invented company context | **Smart intake** — read docs, ask ≤3 |
| “Looks fine” books | Bank recon **RM 0.00**, line-balance proof |
| No system of record | **Beancount** ledger + **Fava** UI |
| One opaque prompt | Skills + state you can resume |

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

| Agent | How to load skills |
|:------|:-------------------|
| **Any skills.sh agent** | `npx skills add cynco-labs/ai-accounting-skills` |
| **Claude Code** (full marketplace) | `/plugin marketplace add` + install umbrella (below) |
| **Any terminal** | `npx @cynco/accounting-skills …` |

Malaysia (MPERS / MFRS / ITA) ships first. Other jurisdictions plug in via the builder hub.

---

## Install

### Skills — any agent

```bash
npx skills add cynco-labs/ai-accounting-skills
npx skills add cynco-labs/ai-accounting-skills --list
npx skills add cynco-labs/ai-accounting-skills --all -g
```

→ [skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

### Claude Code plugins (optional umbrella)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

---

## CLI · `npx`

Zero clone. Deterministic tools agents should shell out to — not re-implement in chat.

```bash
npx @cynco/accounting-skills <command>
```

| Command | What you get |
|:--------|:-------------|
| `demo` | Golden mini ledger → **Fava** |
| `close [client]` | **E2E proof** — validate · gates · ledger |
| `extract ./statements` | Bank PDF/CSV → Excel (+ JSON) |
| `classify ./txns.json` | Deterministic COA classify + review queue |
| `post ./clients/acme` | Classified lines → balancing journals |
| `tb ./clients/acme` | Journals → TB (**never freestyle**) |
| `ledger ./clients/acme --fava` | Journals → Beancount + Fava |
| `firm --init "Your Firm"` | Multi-agent firm profile |
| `init acme-sdn-bhd` | Client workspace scaffold |
| `doctor` | Python / deps health check |
| `check` | Validate engagement or full CI |

Needs **Node ≥ 18** + **Python 3**. `pip install -r requirements.txt` (or whatever `doctor` prints).

<details>
<summary><strong>More CLI detail</strong></summary>

- Package: [`@cynco/accounting-skills`](https://www.npmjs.com/package/@cynco/accounting-skills)
- Kernel: [shared/kernel-contract.md](./shared/kernel-contract.md) · [skill collapse](./shared/skill-collapse-map.md) · [skill craft](./shared/skill-craft.md) · [CONTEXT.md](./CONTEXT.md)
- Agent recipes: [docs/agents/](./docs/agents/)
- Firm profile: [shared/firm-profile.md](./shared/firm-profile.md)
- From a local clone: `node cli/bin/ai-accounting.js doctor`

</details>

---

## Pipeline

```text
  Folder dump
       │
       ▼
  smart-intake  ── infer entity, currency, period; ≤3 questions
       │
       ▼
  extract → classify → post → bank recon (RM0) → roll_tb
       │
       ▼
  year-end AJEs → ATB → standards review → FS + notes
       │
       ▼
  QC (Section A blockers) → finalise → Beancount + Fava
       │
       └──────────────► tax (locked figures only)
```

Six intents: **do-books · extract · classify · post · present · prove**.  
Resume from `engagement_state.json`. Period-first: book the months on disk deeply — don’t stall for twelve calendar months.

---

## Reference

Skills split on one axis — **who can invoke them**.

- **Model-invoked** — agent can reach them when the task fits (stage work, extract, classify, prove).
- **User-invoked** — only when you type them (builder QA, jurisdiction scaffold). They never auto-fire mid-engagement.

| Intent | Job | Engine / artifacts |
|---|---|---|
| **do-books** | Default throw-work entry; intake + orchestrate | `engagement_state.json`, status board |
| **extract** | Source docs → proved lines | `extract_bank.py` → `transactions.json` |
| **classify** | Lines → COA codes | `classify_transactions.py` + review queue |
| **post** | Coded lines → journals; **TB derived** | `post_journals.py`, `roll_tb.py` |
| **present** | ATB → FS, notes, workbook, tax schedules | maps + templates |
| **prove** | Gates + close + ledger SoR | `close_engagement.py`, Beancount, Fava |

Doctrine for writing skills: [`shared/skill-craft.md`](./shared/skill-craft.md).  
Domain language: [`CONTEXT.md`](./CONTEXT.md).  
Architecture: [`shared/architecture.md`](./shared/architecture.md) · [`shared/guardrails.md`](./shared/guardrails.md).

### For agents

| Do | Don't |
|---|---|
| Read docs before interrogating | 20-field setup forms |
| Run repo scripts when they exist | Reinvent Maybank parsers in chat |
| Prove bank/TB balance | Invent lines to “make it work” |
| Hit each skill’s **Done when** | Skip to FS with an open blocker |
| Export Beancount after lock | Treat Excel as the only ledger |
| Write disk artifacts every stage | Rely on chat memory |

```bash
pip install -r requirements.txt
bash scripts/ci_check.sh
```

<details>
<summary><strong>Stage plugins (Claude marketplace)</strong></summary>

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

## Bank extract · Beancount

Maybank Islamic e-statements (pdfplumber + Decimal running-balance proof — not vision-first):

```bash
python3 scripts/extract_maybank_islamic_pdf.py \
  --input /path/to/statements \
  --output ./bank_transactions.xlsx \
  --also-json ./workpapers/transactions.json \
  --fail-on-error
```

```bash
python3 scripts/export_to_beancount.py --client-dir path/to/client --bean-check
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
- [x] Stage plugins + umbrella + skills.sh multi-agent install
- [x] Smart intake + `engagement_state` resume + period-first doctrine
- [x] Kernel CLI: extract · classify · post · tb · close · ledger
- [x] Maybank Islamic PDF + CIMB/generic CSV extractors
- [x] Beancount SoR + Fava · JSON schemas · `ci_check.sh`
- [x] Skill craft + domain language (`CONTEXT.md`) · completion criteria

### Near term

- [ ] More bank PDF adapters (Public Bank, HSBC, RHB, Hong Leong, …)
- [ ] Tax computation worksheet script from locked ATB
- [ ] Intent-canonical install surface (6 names; legacy aliases)

### Next

- [ ] Jurisdiction packs (SG · UK · AU · US)
- [ ] AR/AP aging packs · FAR → dep → CA end-to-end
- [ ] SST / e-Invoice (MY) assist skills
- [ ] Multi-entity consolidation skeleton

### Later

- [ ] Connector pack (drop folders, cloud intake)
- [ ] Managed-agent cookbooks (deadline watcher, monthly close)
- [ ] Eval harness: extract accuracy + classify precision

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
