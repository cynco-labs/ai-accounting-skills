# Claude for Accounting

Reference **agents, skills, and workflows** for the accounting engagements we see most — bookkeeping, reconciliations, year-end adjustments, financial reporting standards review, financial statements and notes, quality control, finalisation, and tax computation.

> **New here?** Start with [QUICKSTART.md](./QUICKSTART.md) — install in about 60 seconds. This README is the full reference.

Everything here is available as [Claude Code](https://claude.com/product/claude-code) / [Claude Cowork](https://claude.com/product/cowork) plugins. Same skills whether you run one stage or the full engagement pipeline.

This repository is **open source** and designed to scale across firms, jurisdictions, and industries. Malaysia (MPERS / MFRS / ITA 1967) ships as the first full reference pack; other jurisdictions extend the same stage architecture.

## Important notice

**Every output from these plugins is a draft for professional accountant review — not signed financial statements, not an audit or review opinion, not tax advice, and not a substitute for a licensed professional.**

Plugins are built with guardrails that reflect that:

- Source provenance on load-bearing numbers
- Zero-tolerance mathematical gates (trial balance, balance sheet, bank reconciliation)
- Explicit gates before lock, management approval, auditor handoff, or tax filing
- Framework and tax rules tagged for verification against authoritative sources

The reviewing accountant verifies figures against source documents, applies professional judgment, and takes responsibility for anything issued to clients, auditors, companies registries, or tax authorities. These plugins make that review faster; they do not replace it.

**These plugins do not represent any regulator’s, standard-setter’s, or professional body’s official positions.** Checklists and suggested treatments are aids to the reviewing professional’s own analysis.

## What's in the repo

| Area | What you get |
|---|---|
| **Stage plugins** | One plugin per engagement phase — install only what you need |
| **Skills** | Domain methods + slash commands (`/plugin:skill`) |
| **Firm practice profile** | Cold-start interview writes plain-English firm defaults every skill reads |
| **Jurisdiction packs** | Malaysia first; scaffold for others via `accounting-builder-hub` |
| **Note templates** | MPERS notes scaffolding for the time-consuming disclosure work |
| **Industry COA packs** | Optional account overlays (trading, services, F&B, property, professional firms) |
| **Connectors** | Documented MCP integration points (banks, DMS, ledgers) |
| **Managed-agent cookbooks** | Scheduled workflows (filing deadlines, bank intake) |
| **Builder hub** | Skill design QA + jurisdiction extension tooling for contributors |

## Engagement pipeline

```
Source Documents
      ↓
Bookkeeping (sales · purchases · receipts · payments · journals)
      ↓
Bank & Ledger Reconciliations
      ↓
Preliminary Trial Balance
      ↓
Year-End Adjustments
      ↓
Adjusted Trial Balance
      ↓
Standards Technical Review (MPERS / MFRS / extension)
      ↓
Financial Statements + Notes
      ↓
Quality Review
      ↓
Final Signed Financial Statements
      ↓
Tax Computation & Statutory Filings
```

Canonical routing: [`references/pipeline.md`](./references/pipeline.md).

## Plugins

| Plugin | What it adds |
|---|---|
| **[engagement-accounting](./engagement-accounting)** | Firm cold-start, engagement setup, source-doc inventory, client workspaces, full-pipeline orchestrator |
| **[bookkeeping-accounting](./bookkeeping-accounting)** | Record & classify transactions; COA; journals |
| **[reconciliation-accounting](./reconciliation-accounting)** | Bank + subledgers (AR/AP/inventory/FA/loans/tax); preliminary TB |
| **[year-end-accounting](./year-end-accounting)** | YE adjustments; adjusted trial balance |
| **[mpers-accounting](./mpers-accounting)** | MPERS/MFRS technical review + disclosure checklist |
| **[financial-statements-accounting](./financial-statements-accounting)** | Primary statements, notes, compilation report, Excel workbook |
| **[quality-review-accounting](./quality-review-accounting)** | QC blockers, cross-ties, note consistency |
| **[finalisation-accounting](./finalisation-accounting)** | Lock, management approval, auditor pack, statutory handoff |
| **[tax-accounting](./tax-accounting)** | Tax computation + capital allowances (Malaysia pack shipped) |
| **[beancount-ledger](./beancount-ledger)** | Beancount system of record + Fava UI after finalisation |
| **[accounting-builder-hub](./accounting-builder-hub)** | Skill QA, jurisdiction scaffold, contributor tooling |

## Agents (common commands)

| Agent | Plugin | Command |
|---|---|---|
| Firm cold-start | engagement | `/engagement-accounting:cold-start-interview` |
| Engagement setup | engagement | `/engagement-accounting:engagement-setup` |
| Full pipeline | engagement | `/engagement-accounting:full-engagement-pipeline` |
| Classify transactions | bookkeeping | `/bookkeeping-accounting:classify-transactions` |
| Bank reconciliation | reconciliation | `/reconciliation-accounting:bank-reconciliation` |
| Year-end adjustments | year-end | `/year-end-accounting:year-end-adjustments` |
| MPERS technical review | mpers | `/mpers-accounting:mpers-technical-review` |
| Primary statements | FS | `/financial-statements-accounting:prepare-primary-statements` |
| Notes to FS | FS | `/financial-statements-accounting:prepare-notes` |
| Quality review | QC | `/quality-review-accounting:quality-review` |
| Tax computation | tax | `/tax-accounting:tax-computation` |
| Skill design QA | builder | `/accounting-builder-hub:skills-qa` |

See each plugin `README.md` for the full skill list.

## Repository layout

```
engagement-accounting/              # setup + orchestrator
bookkeeping-accounting/
reconciliation-accounting/
year-end-accounting/
mpers-accounting/
financial-statements-accounting/
quality-review-accounting/
finalisation-accounting/
tax-accounting/
accounting-builder-hub/             # contributor / extension hub
managed-agent-cookbooks/            # scheduled agent templates
references/
  jurisdictions/malaysia/           # first full pack (MPERS, tax, entity types…)
  notes-templates/mpers/            # disclosure scaffolds
  coa_templates/                    # entity COAs
  coa_templates/industry/           # industry overlays
  pipeline.md
scripts/                            # validate.py, workbook/PDF generators
shared/
  guardrails.md
  skill-design-framework.md
  jurisdiction-extension-guide.md
  firm-profile-template.md
.claude-plugin/marketplace.json
```

Each stage plugin:

```
<plugin>/
  .claude-plugin/plugin.json
  CLAUDE.md                 # practice profile TEMPLATE (runtime config written elsewhere)
  README.md
  skills/<skill>/SKILL.md
  references/               # optional deep refs
  agents/                   # optional scheduled agents
```

## How it fits together

| | What it is | Where it lives |
|---|---|---|
| **Plugins** | Self-contained stage bundles | `<plugin>/` |
| **Skills** | Step-by-step methods + slash commands | `<plugin>/skills/<skill>/SKILL.md` |
| **Firm profile** | Plain-English firm defaults every skill reads | `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` |
| **Practice profile** | Per-plugin preferences | `~/.claude/plugins/config/claude-for-accounting/<plugin>/CLAUDE.md` |
| **Jurisdiction pack** | Standards + tax + entity rules for a country | `references/jurisdictions/<id>/` |
| **Connectors** | MCP servers for banks, DMS, ledgers | [CONNECTORS.md](./CONNECTORS.md) |
| **Cookbooks** | Headless / scheduled agent templates | `managed-agent-cookbooks/` |

Everything is markdown and JSON (plus optional Python generators). No build step for skill content.

## Agent-native by default

Humans will not type slash commands. They will dump a client folder and say “do the year end.”

| Mechanism | Why it exists |
|---|---|
| **`accounting-engagement` umbrella** | One install → all stage skills (synced from modular plugins) |
| Fat-trigger descriptions on every skill | Host agents auto-select from natural language |
| **`full-engagement-pipeline` as DEFAULT entry** | Full jobs route here unless the ask is clearly one stage |
| **`smart-intake` + `shared/smart-intake.md`** | Folder dump with no company context: infer from docs, ≤3 smart questions |
| `engagement_state.json` + SessionStart hook | Resume mid-job; banner when state is nearby |
| JSON schemas + `validate_engagement_artifacts.py` | Machine-checkable transactions / journals / TB |
| `extract-bank-statement` + Maybank PDF script | Proven text/regex/balance-proof extract (fast, not vision-first) |
| `normalize_bank_csv.py` | CSV bank exports |
| **Beancount + Fava** | Ledger SoR + interactive UI after final books |
| `fixtures/golden-mini-sdn-bhd` | Golden path for regression |
| `evals/utterance_routing.json` | Discoverability tests (top-K description match) |
| `shared/agent-runtime.md` | Runtime contract for any agent host |

```bash
# Recommended install surface
/plugin install accounting-engagement@claude-for-accounting

# Maintainers / CI
python3 scripts/sync_umbrella.py --check
python3 scripts/validate_engagement_artifacts.py fixtures/golden-mini-sdn-bhd
python3 scripts/eval_utterance_routing.py
```

Read: [shared/agent-runtime.md](./shared/agent-runtime.md).

## Design principles (scalability & maintainability)

1. **Stage plugins, not entity plugins** — entity and industry differences live in COA + jurisdiction refs; the pipeline stays universal.
2. **SKILL.md carries doctrine; CLAUDE.md is the net** — see [CONTRIBUTING.md](./CONTRIBUTING.md) and `shared/skill-design-framework.md`.
3. **Hard gates over soft hope** — unbalanced TB / bank / BS are blockers, not warnings.
4. **Jurisdiction is data, not a fork** — add a pack; don’t clone the whole repo.
5. **White-label by default** — firm name, registration, and house style come from cold-start, never hard-coded product branding in skill outputs.
6. **Validate in CI** — `scripts/validate_marketplace.py` enforces structure before merge.
7. **Agent-native first** — throw-work routing beats menu-driven UX.

## Getting started

See **[QUICKSTART.md](./QUICKSTART.md)**.

```text
/plugin marketplace add <path-or-url-to-this-repo>
/plugin install engagement-accounting@claude-for-accounting
/engagement-accounting:cold-start-interview
```

## Default jurisdiction

| Entity (Malaysia) | Framework (typical) | Tax form |
|---|---|---|
| Berhad (public) | MFRS | Form C |
| Sdn Bhd | MPERS | Form C |
| PLT | MPERS | Form PT |
| Sole prop | Accrual per S21A ITA | Form B |
| Partnership | Accrual per S21A ITA | Form P |
| Koperasi | MCA standards | Form TF |
| Trust | MFRS/MPERS (varies) | Form TP |

Other countries: read `shared/jurisdiction-extension-guide.md` and run `/accounting-builder-hub:jurisdiction-scaffold`.

## Core principles

1. Every number traces to a source document.  
2. Check documents before asking questions (smart intake — infer first).  
3. Standards and tax compliance — no material shortcuts.  
4. Zero tolerance for imbalance (TB, BS, bank).  
5. Document decisions in working papers.  
6. **Excel = working papers; Beancount = ledger system of record; Fava = UI.**

## Production checks (maintainers)

```bash
pip install -r requirements.txt
bash scripts/ci_check.sh
```

Must pass before release or merge.

## Contributing

We welcome PRs that improve skills, jurisdiction packs, note templates, COAs, validators, and cookbooks.

- [CONTRIBUTING.md](./CONTRIBUTING.md) — design rules and PR checklist  
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)  
- [SECURITY.md](./SECURITY.md)  
- [CLA.md](./CLA.md) — contributor license agreement  
- [CHANGELOG.md](./CHANGELOG.md)

Run validators before opening a PR:

```bash
python3 scripts/validate_marketplace.py
```

## Maintainer

**Hazli Johar** — [coding@hazli.dev](mailto:coding@hazli.dev)  
Version: **v0.0.1** — see [CHANGELOG.md](./CHANGELOG.md) and [MAINTAINERS.md](./MAINTAINERS.md).

## License

Apache License 2.0 — see [LICENSE](./LICENSE).

Accounting standards and tax summaries are **workflow aids**. Authoritative text remains with standard-setters and tax authorities (e.g. MASB, MIA, LHDN for the Malaysia pack).

## Relationship to monolithic skills

A single-file “accounting workflow” skill may still be useful for tiny installs. This marketplace **splits that workflow into stage plugins** so each phase can be reviewed, versioned, and extended independently — the same idea as practice-area plugins in [claude-for-legal](https://github.com/anthropics/claude-for-legal).
