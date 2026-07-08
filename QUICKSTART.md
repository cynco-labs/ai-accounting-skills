# Quick Start

**About 60 seconds to install. 2–15 minutes to configure your firm.**

## Install in Claude Code

1. **Open Claude Code.**

2. **Add the marketplace.** Type `/plugin marketplace add ` (space at the end), then drag this repo folder onto the terminal, or pass a path / GitHub URL:

   ```text
   /plugin marketplace add /path/to/claude-for-accounting
   # or, once published:
   # /plugin marketplace add https://github.com/<org>/claude-for-accounting
   ```

3. **Install plugins** you need. Start with engagement + the stages you run:

   ```text
   /plugin install engagement-accounting@claude-for-accounting
   /plugin install bookkeeping-accounting@claude-for-accounting
   /plugin install reconciliation-accounting@claude-for-accounting
   /plugin install year-end-accounting@claude-for-accounting
   /plugin install mpers-accounting@claude-for-accounting
   /plugin install financial-statements-accounting@claude-for-accounting
   /plugin install quality-review-accounting@claude-for-accounting
   /plugin install finalisation-accounting@claude-for-accounting
   /plugin install tax-accounting@claude-for-accounting
   ```

   Contributors / pack authors also install:

   ```text
   /plugin install accounting-builder-hub@claude-for-accounting
   ```

4. **Restart Claude Code** so slash commands load.

5. **Run firm setup** (required for non-generic output):

   ```text
   /engagement-accounting:cold-start-interview
   ```

   Quick path ≈ 2 minutes (defaults + firm identity). Full path ≈ 10–15 minutes (policies, escalation, seed workpapers).

6. **Open an engagement:**

   ```text
   /engagement-accounting:engagement-setup
   ```

7. **Run the pipeline** end-to-end or stage-by-stage:

   ```text
   /engagement-accounting:full-engagement-pipeline
   ```

## Install user-scoped, not project-scoped

When `/plugin install` asks for scope, **prefer user scope**. Project scope cannot read client files outside the project folder (Downloads, DMS sync folders, etc.). User scope does not grant extra access to arbitrary files — you still point at paths — it only makes the plugin available from any working directory.

## Which plugin is for me?

| You need to… | Install… | First command |
|---|---|---|
| Configure the firm / start a client | `engagement-accounting` | `/engagement-accounting:cold-start-interview` |
| Book from bank & invoices | `bookkeeping-accounting` | `/bookkeeping-accounting:record-transactions` |
| Reconcile bank & ledgers | `reconciliation-accounting` | `/reconciliation-accounting:bank-reconciliation` |
| Post year-end journals | `year-end-accounting` | `/year-end-accounting:year-end-adjustments` |
| Review against MPERS/MFRS | `mpers-accounting` | `/mpers-accounting:mpers-technical-review` |
| Draft FS & notes | `financial-statements-accounting` | `/financial-statements-accounting:prepare-primary-statements` |
| QC before issue | `quality-review-accounting` | `/quality-review-accounting:quality-review` |
| Lock / approve / auditor pack | `finalisation-accounting` | `/finalisation-accounting:finalise-accounts` |
| Tax computation | `tax-accounting` | `/tax-accounting:tax-computation` |
| Extend jurisdictions / QA skills | `accounting-builder-hub` | `/accounting-builder-hub:skills-qa` |

## What you’re installing

Each plugin can learn your firm through setup, writes a practice profile under:

```text
~/.claude/plugins/config/claude-for-accounting/
```

Every skill reads that profile before producing work product. Edit the profile in plain English anytime.

**Every output is a draft for accountant review.** Plugins flag uncertainty, gate irreversible steps, and refuse to invent numbers. A professional reviews, verifies, and takes responsibility.

## Stuck?

| Symptom | Fix |
|---|---|
| Command not found after install | Restart Claude Code |
| “Run setup first” / generic output | `/engagement-accounting:cold-start-interview` |
| Numbers look invented / context lost | Re-read source documents — never reconstruct from memory |
| “I can’t read [file]” | Reinstall user-scoped, or move the file into the working tree |
| Unbalanced TB / bank | Treat as blocker — fix before FS (see `shared/guardrails.md`) |
| Wrong country rules | Install/build a jurisdiction pack — `shared/jurisdiction-extension-guide.md` |

## What’s in the box

10 plugins, managed-agent cookbooks, Malaysia jurisdiction pack, MPERS note templates, industry COA overlays, validators. Full reference: [README.md](./README.md).
