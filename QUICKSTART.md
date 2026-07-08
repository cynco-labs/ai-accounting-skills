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

3. **Install** — prefer the **umbrella** (one plugin, all stage skills):

   ```text
   /plugin install accounting-engagement@claude-for-accounting
   ```

   Or install modular stage plugins (see `scripts/install_all.sh`). Contributors also:

   ```text
   /plugin install accounting-builder-hub@claude-for-accounting
   ```

4. **Restart Claude Code** so slash commands load.

5. **Run firm setup** (required for non-generic output):

   ```text
   /accounting-engagement:cold-start-interview
   ```

   Quick path ≈ 2 minutes. Full path ≈ 10–15 minutes.

6. **Throw work at the agent** (agent-native path):

   Drop a client folder and say e.g. *“Do the year end for this Sdn Bhd and prepare MPERS financial statements.”*  
   DEFAULT skill: `full-engagement-pipeline`. Writes `engagement_state.json` for resume.

7. **Or drive stages explicitly:**

   ```text
   /accounting-engagement:engagement-setup
   /accounting-engagement:extract-bank-statement
   /accounting-engagement:full-engagement-pipeline
   ```

8. **Validate artifacts** (from this repo):

   ```bash
   python3 scripts/validate_engagement_artifacts.py path/to/client
   python3 scripts/validate_engagement_artifacts.py fixtures/golden-mini-sdn-bhd
   ```

9. **After books are final — Beancount (ledger SoR) + Fava (UI):**

   ```bash
   pip install beancount fava   # once
   python3 scripts/export_to_beancount.py \
     --client-dir path/to/client \
     --output path/to/client/ledger/main.beancount \
     --bean-check
   scripts/run_fava.sh path/to/client/ledger/main.beancount
   # open http://127.0.0.1:5000
   ```

   Excel workpapers remain for review; **Beancount is the system of record.**

## Install user-scoped, not project-scoped

When `/plugin install` asks for scope, **prefer user scope**. Project scope cannot read client files outside the project folder (Downloads, DMS sync folders, etc.). User scope does not grant extra access to arbitrary files — you still point at paths — it only makes the plugin available from any working directory.

## Which plugin is for me?

| You need to… | Install… | First command |
|---|---|---|
| **Everything (recommended)** | `accounting-engagement` | dump client folder / `full-engagement-pipeline` |
| Configure the firm | umbrella or `engagement-accounting` | `cold-start-interview` |
| Resume mid-job | umbrella | `resume-engagement` |
| Extract bank PDF/CSV | umbrella | `extract-bank-statement` |
| Modular stage only | individual `*-accounting` plugins | see plugin README |
| Extend jurisdictions / QA skills | `accounting-builder-hub` | `skills-qa` |

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
