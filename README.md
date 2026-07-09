<p align="center">
  <img src="https://img.shields.io/badge/v2.2.4-0d6efd?style=for-the-badge" alt="v2.2.4" />
  <a href="https://skills.sh/cynco-labs/ai-accounting-skills"><img src="https://skills.sh/b/cynco-labs/ai-accounting-skills" alt="skills.sh" /></a>
  <img src="https://img.shields.io/badge/Beancount-ledger-111827?style=for-the-badge" alt="Beancount" />
  <img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" alt="MIT License" />
</p>

<h1 align="center">AI Accounting Skills</h1>

<p align="center">
  <strong>Real bookkeeping for coding agents — not made-up numbers.</strong><br/>
  Drop a folder of bank statements → balanced books → financials → Beancount + Fava.
</p>

<p align="center">
  Put bank statements and receipts in a folder. Say <em>“do the year end.”</em><br/>
  The agent follows a proper process: checks, proofs, and files saved on disk.
</p>

---

## Quick start (about 30 seconds)

1. Install:

```bash
npx skills add cynco-labs/ai-accounting-skills
```

2. Point your agent at a folder of bank statements / receipts and say:

> Do the accounting.

3. Optional — command-line tools (no need to clone the repo):

```bash
npx @cynco/accounting-skills extract ./statements --json ./txns.json
npx @cynco/accounting-skills classify ./txns.json
npx @cynco/accounting-skills post ./clients/acme --opening-from-bank
npx @cynco/accounting-skills tb ./clients/acme --both
npx @cynco/accounting-skills close ./clients/acme
```

That’s it. You can stop mid-way and continue later — progress is saved in `engagement_state.json`.

---

## Why this exists

Coding agents are good at code. They are often **bad at accounts**.

They invent company names, type trial balance totals into Excel, and skip bank reconciliation. This project is a set of agent skills that behave more like a junior who was trained properly.

### #1: The agent invents the company

**What goes wrong.** You drop a folder. The agent asks twenty questions, or invents the company name, year-end, and reporting framework.

**What we do instead.** Read the documents first. Guess what is clear. Confirm only what is unclear — at most **3** good questions. Start extracting bank statements in the same session.

→ `smart-intake` · `full-engagement-pipeline`

### #2: The numbers don’t tie

**What goes wrong.** Nice-looking Excel. Trial balance doesn’t balance. Bank GL doesn’t match the bank statement. Nobody can defend the file.

**What we do instead.** Extract, classify, post, and build the trial balance with **scripts** — not chat guesses. The TB is **calculated from journals**, never typed by hand. Bank recon must be **RM 0.00** (or clearly marked as limited). QC Section A must pass before anything is called final.

→ `extract` · `classify` · `post` · `tb` · `quality-review`

### #3: Chat becomes the books

**What goes wrong.** Long chat. Context is lost. The agent “remembers” numbers that no longer match the files.

**What we do instead.** Every step writes files on disk (transactions, journals, TB, recon, FS). The **files are the books**, not the chat. After a break, re-read the files.

→ [Core rules](./shared/kernel-contract.md) · [Plain English terms](./CONTEXT.md)

### #4: One giant vague prompt

**What goes wrong.** “Do the accounts” as one mess. You can’t resume, review, or fix one step.

**What we do instead.** Six clear jobs: **do the books · extract · classify · post · present · prove**. One step at a time. Builder tools (skill QA, new country packs) only run when you ask for them.

→ [Six main jobs](./shared/skill-collapse-map.md) · [How we write skills](./shared/skill-craft.md)

### In short

| Without this | With this |
|---|---|
| Random Excel, no checks | Workpapers in JSON → **balanced TB** or stop |
| Invented company details | **Read first**, ask ≤3 questions |
| “Looks fine” books | Bank recon **RM 0.00**, line-by-line proof |
| Excel as the only ledger | **Beancount** ledger + **Fava** in the browser |
| One vague prompt | Skills + saved progress you can resume |

---

## Works with your agent

Install once via [skills.sh](https://skills.sh/cynco-labs/ai-accounting-skills) — same package works across the major coding agents.

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

Malaysia (MPERS / MFRS / ITA) ships first. Other countries can be added as data packs.

---

## Install

### Skills — any agent

```bash
npx skills add cynco-labs/ai-accounting-skills
npx skills add cynco-labs/ai-accounting-skills --list
npx skills add cynco-labs/ai-accounting-skills --all -g
```

→ [skills.sh/cynco-labs/ai-accounting-skills](https://skills.sh/cynco-labs/ai-accounting-skills)

### Claude Code plugins (optional)

```text
/plugin marketplace add https://github.com/cynco-labs/ai-accounting-skills
/plugin install accounting-engagement@claude-for-accounting
```

---

## Command line · `npx`

No need to clone. These are the tools the agent should **run**, not re-type in chat.

```bash
npx @cynco/accounting-skills <command>
```

| Command | What you get |
|:--------|:-------------|
| `demo` | Sample mini ledger → open in **Fava** |
| `close [client]` | End-to-end check — validate, must-pass checks, ledger summary |
| `extract ./statements` | Bank PDF/CSV → Excel (+ JSON) |
| `classify ./txns.json` | Suggest COA codes + list what needs review |
| `post ./clients/acme` | Classified lines → balancing journals |
| `tb ./clients/acme` | Journals → trial balance (**calculated — never typed by hand**) |
| `ledger ./clients/acme --fava` | Journals → Beancount + Fava |
| `firm --init "Your Firm"` | Firm name / defaults for the agent |
| `init acme-sdn-bhd` | New client folder layout |
| `doctor` | Check Python / dependencies |
| `check` | Validate a client job or run full CI |

Needs **Node ≥ 18** + **Python 3**. `pip install -r requirements.txt` (or follow what `doctor` prints).

<details>
<summary><strong>More detail</strong></summary>

- Package: [`@cynco/accounting-skills`](https://www.npmjs.com/package/@cynco/accounting-skills)
- Core rules: [shared/kernel-contract.md](./shared/kernel-contract.md) · [six main jobs](./shared/skill-collapse-map.md) · [plain English terms](./CONTEXT.md) · [how we write skills](./shared/skill-craft.md)
- Agent setup notes: [docs/agents/](./docs/agents/)
- Firm profile: [shared/firm-profile.md](./shared/firm-profile.md)
- From a local clone: `node cli/bin/ai-accounting.js doctor`

</details>

---

## How a job flows

```text
  Folder of banks / receipts
       │
       ▼
  Smart intake  ── read files; guess company & period; ≤3 questions
       │
       ▼
  Extract banks → classify → journals → bank recon (RM0) → trial balance
       │
       ▼
  Year-end adjustments → adjusted TB → standards review → FS + notes
       │
       ▼
  QC (math checks must pass) → lock → Beancount + Fava
       │
       └──────────────► tax (only from locked figures)
```

**Six main jobs:** do the books · extract · classify · post · present · prove.

**Work the months you have.** If the client only gave March–July, book those months properly. Don’t refuse to start because you don’t have 12 months yet. Full-year financials only when coverage is enough (or the user accepts a clear limitation).

Resume anytime from `engagement_state.json`.

---

## The six main jobs

| Job | Plain English | Main files / tools |
|---|---|---|
| **Do the books** | Start or continue the whole engagement | `engagement_state.json`, status board |
| **Extract** | Pull lines out of bank PDFs/CSV with balance proof | `extract_bank.py` → `transactions.json` |
| **Classify** | Understand the money (when needed), then COA codes |  +  |
| **Post** | Turn coded lines into double-entry journals; **TB is calculated** | `post_journals.py`, `roll_tb.py` |
| **Present** | Build FS, notes, Excel pack, tax schedules from the adjusted TB | templates + maps |
| **Prove** | QC, lock, export the official ledger | close script, Beancount, Fava |

### Two kinds of skills

- **Agent can pick them up** when the task fits (day-to-day accounting steps).
- **You type them on purpose** (builder tools like skill QA or new country packs) — they don’t jump in mid-client job.

How to write skills: [`shared/skill-craft.md`](./shared/skill-craft.md).  
Words we use: [`CONTEXT.md`](./CONTEXT.md).  
Safety rules: [`shared/guardrails.md`](./shared/guardrails.md).

### Rules for the agent

| Do | Don't |
|---|---|
| Read the documents before asking a long form | Open with 20 blank questions |
| Run the repo scripts when they exist | Re-type a Maybank statement by hand in chat |
| Prove bank and TB balance | Invent lines so the TB “looks right” |
| Finish each step’s **Done when** | Jump to financials with an open hard stop |
| Export Beancount after lock | Treat Excel as the only ledger |
| Save files after every step | Rely on chat memory |

```bash
pip install -r requirements.txt
bash scripts/ci_check.sh
```

<details>
<summary><strong>Plugins (Claude marketplace)</strong></summary>

| Plugin | Job |
|---|---|
| [`accounting-engagement`](./accounting-engagement) | **All-in-one install** — use this |
| [`engagement-accounting`](./engagement-accounting) | Firm setup, smart intake, full pipeline |
| [`bookkeeping-accounting`](./bookkeeping-accounting) | Extract, classify, journals |
| [`reconciliation-accounting`](./reconciliation-accounting) | Bank + subledgers + TB |
| [`year-end-accounting`](./year-end-accounting) | Year-end adjustments + adjusted TB |
| [`mpers-accounting`](./mpers-accounting) | Standards review + disclosures |
| [`financial-statements-accounting`](./financial-statements-accounting) | Primary statements, notes, workbook |
| [`quality-review-accounting`](./quality-review-accounting) | QC checks |
| [`finalisation-accounting`](./finalisation-accounting) | Lock, approval, auditor pack |
| [`tax-accounting`](./tax-accounting) | Malaysian tax + capital allowances |
| [`beancount-ledger`](./beancount-ledger) | Export ledger + Fava |
| [`accounting-builder-hub`](./accounting-builder-hub) | Skill QA + new country pack scaffold |

Marketplace id: **`claude-for-accounting`**

</details>

---

## Bank extract · Beancount

Maybank Islamic e-statements (text layer + running-balance proof — not “look at the PDF with AI and guess”):

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

## Check the repo

```bash
git clone https://github.com/cynco-labs/ai-accounting-skills.git
cd ai-accounting-skills
pip install -r requirements.txt
bash scripts/ci_check.sh
```

Sample data: `fixtures/golden-mini-sdn-bhd` (made-up — not a real client).

---

## Roadmap

### Shipped

- [x] Full engagement flow (intake → books → QC → lock)
- [x] Stage plugins + all-in-one install + skills.sh
- [x] Smart intake + resume from saved state
- [x] Work the months you have (don’t force 12 months to start)
- [x] CLI: extract · classify · post · tb · close · ledger
- [x] Maybank Islamic PDF + CIMB/generic CSV extractors
- [x] Beancount ledger + Fava · JSON checks · `ci_check.sh`
- [x] Plain English terms (`CONTEXT.md`) · **Done when** on every skill

### Near term

- [ ] More bank PDF adapters (Public Bank, HSBC, RHB, Hong Leong, …)
- [ ] Tax computation worksheet from locked adjusted TB
- [ ] Simpler install names for the six main jobs (old names still work)

### Next

- [ ] Country packs (SG · UK · AU · US)
- [ ] AR/AP aging packs · fixed assets → depreciation → capital allowances
- [ ] SST / e-Invoice (MY) helpers
- [ ] Group / multi-entity skeleton

### Later

- [ ] Drop-folder / cloud intake helpers
- [ ] Managed-agent recipes (deadline watcher, monthly close)
- [ ] Accuracy tests on sample extracts and classifications

---

## Disclaimer

**Drafts for a professional accountant to review only.**

Not signed financial statements. Not an audit or review opinion. Not tax advice.  
Not a substitute for a licensed professional. Not official MASB / MIA / LHDN positions.

The reviewing accountant checks figures against sources and takes responsibility for anything issued.

---

## Maintainers & license

**Hazli Johar** — [coding@hazli.dev](mailto:coding@hazli.dev) · [cynco-labs](https://github.com/cynco-labs)

MIT License — [LICENSE](./LICENSE) · Contributions — [CONTRIBUTING.md](./CONTRIBUTING.md)

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
