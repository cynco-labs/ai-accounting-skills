# Claude for Accounting — Repo Guide for Agents

This repository is an **open-source plugin marketplace** for accounting engagements: stage plugins, skills, firm profiles, country packs, and shared safety rules.

## First principles (read these)

1. **`shared/runtime-brief.md`** — **throw-work load first** (one screen). Don’t preload 10 doctrine files.
2. **`shared/kernel-contract.md`** — **core rules**: which files hold amounts; TB only via scripts.
3. **`shared/skill-collapse-map.md`** — six main jobs. Don’t invent a seventh without updating that map.
4. **`shared/operator-lens.md`** — one engine: **`operator`** + **depth**. No business-vs-firm slash forks.
5. **`shared/shelf-first.md`** — docs may be anywhere; **one intake** shelves before extract.
6. **`CONTEXT.md`** — plain English terms.
7. **Depth-scoped done** — machine gates in `references/depth_gates.json`; `python3 scripts/depth_gates.py <client> --strict`. Books-only ≠ year-end pack.
8. **Trial balances are calculated only** — `scripts/roll_tb.py` / `npx @cynco/accounting-skills tb`.
9. **Progress questions use structured tools** — `shared/user-questions.md`.
10. **Work the months you have** — don’t pressure for 12 months.

## When working in this repo

1. Read `shared/guardrails.md` before changing skills that produce numbers.
2. Read `CONTRIBUTING.md`, `shared/skill-craft.md`, and `shared/skill-design-framework.md` before new skills.
3. Prefer country packs over hard-coding country rules into stage skills.
4. Never commit client data, secrets, or hard-coded firm branding.
5. Run `python3 scripts/validate_marketplace.py` after structural edits.
6. After skill edits: `python3 scripts/sync_umbrella.py`.
7. Builder skills (`skills-qa`, jurisdiction scaffold, builder cold-start) only run when the user asks — they must not auto-start mid-client job.
8. **Short slash surface** — prefer `/do-books` · `/extract` · `/classify` · `/post` · `/present` · `/prove` (see `shared/slash-surface.md`). Aliases load canonical long skills; don’t duplicate doctrine.
9. **After release push to `main`:** run `npm publish --access public` locally so browser auth can open (Hazli authenticates). See `PUBLISH.md`. Don’t only rely on CI npm unless he says so.

## Plugin map → engagement flow

| Stage | Plugin |
|---|---|
| Firm + engagement setup | `engagement-accounting` |
| Record & classify | `bookkeeping-accounting` |
| Reconcile + preliminary TB | `reconciliation-accounting` |
| Year-end + adjusted TB | `year-end-accounting` |
| Standards review | `mpers-accounting` (name is historical; content is standards pack + review) |
| Statements + notes | `financial-statements-accounting` |
| QC | `quality-review-accounting` |
| Finalise | `finalisation-accounting` |
| Tax | `tax-accounting` |
| Contributor tooling | `accounting-builder-hub` |

## Layout

```
claude-for-accounting/
  .claude-plugin/marketplace.json
  shared/                 # guardrails, design framework, country guide
  references/
    jurisdictions/        # country packs (malaysia first)
    notes-templates/      # disclosure scaffolds
    coa_templates/        # entity + industry
  scripts/                # validate + workbook/PDF generators
  managed-agent-cookbooks/
  <plugin>/skills/<skill>/SKILL.md
```

## Runtime config (not in git)

```
~/.claude/plugins/config/claude-for-accounting/
  firm-profile.md
  <plugin>/CLAUDE.md
  clients/<slug>/          # optional
```

## Design principles

1. **Real engagement flow** — stages match how firms actually work.  
2. **Every number has a source** — bank page, prior FS, or formula on those.  
3. **White-label** — firm identity from setup only.  
4. **Country rules as data** — packs under `references/jurisdictions/`.  
5. **SKILL.md carries the real instructions** — CLAUDE.md is the safety net.  
6. **Validate in CI** — structure checks before merge.  
7. **Predictable process** — lean skill descriptions, clear **Done when**, one stage at a time (`shared/skill-craft.md`).  
8. **Plain English first** — prefer `CONTEXT.md` words over engineering slang in user-facing text.

## Default firm seed

There is **no** default firm. Cold-start writes placeholders until the user answers.
