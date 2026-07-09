# Claude for Accounting — domain language

Shared language for agents and humans. Prefer these terms in skills, tickets, commits, and chat.  
Canonical mechanics: `shared/kernel-contract.md`. Intent map: `shared/skill-collapse-map.md`.  
Skill writing craft: `shared/skill-craft.md`.

## Language

**Engagement**  
One client + one period (or FY) under work. Lives in a folder with `engagement_state.json`.  
_Avoid_: job, matter, project (unless quoting a firm’s own term)

**Intent**  
One of six product verbs: **do-books · extract · classify · post · present · prove**.  
Legacy skill names may still ship; new work targets intents.  
_Avoid_: stage skill name as the product identity when the intent is clearer

**Kernel**  
The pure functions and truth shapes that carry amounts: extract → classify → post → roll_tb → prove/export.  
_Avoid_: freestyle TB, “just total the Excel”

**Truth shape**  
A named artifact that may hold balances or lines (`transactions.json`, `journals.json`, `tb_*.json`, `ledger/main.beancount`, …).  
_Avoid_: “the file”, “the dump” without the shape name

**roll_tb**  
Derive a trial balance only by reducing journals (`scripts/roll_tb.py`). Never type TB totals.  
_Avoid_: “prepare a TB”, “build TB in Excel first”

**Period-first**  
Book the months present on disk deeply. Do not stall for twelve calendar months. Full-year FS is opt-in when coverage allows.  
_Avoid_: “incomplete year, cannot start”

**Disk is truth**  
Artifacts on disk beat chat memory. After compaction, re-read sources and workpapers.  
_Avoid_: reconstructing figures from conversation

**Blocker**  
Hard gate. Stop; do not call work final.  
_Avoid_: warning, issue (when you mean hard stop)

**AMBER**  
Documented limitation that allows continuing a path without claiming full-year / signed completeness.  
_Avoid_: soft fail, caveat (when the formal limitation is meant)

**Provenance**  
Source link or formula tag on a material figure (`[source: …]`, `[model calculation — verify]`).  
_Avoid_: “from the books” without a path

**Structured ask**  
Progress-gating question via the host question tool (≤3, options, recommended first). See `shared/user-questions.md`.  
_Avoid_: long prose questionnaires mid-pipeline

**Status board**  
Short markdown board after advancing work: stages, blockers, next action.  
_Avoid_: wall of slash-commands for clients

**Jurisdiction pack**  
Country rules as data under `references/jurisdictions/<id>/`, not forked stage skills.  
_Avoid_: hard-coding rates into SKILL.md

**Firm profile**  
White-label identity from cold-start config — not committed client branding.  
_Avoid_: default firm seed in git

## Relationships

- An **Engagement** advances through **Intents**; each intent reads/writes **Truth shapes**.
- **Kernel** pure functions produce derived shapes; agents author classifications and YE judgement, not TB totals.
- **Blockers** freeze finalisation; **AMBER** documents partial scope under **period-first**.

## Flagged ambiguities

- **Stage** vs **intent** — stage keys in `engagement_state.json` are fine-grained; product surface collapses to six intents.
- **Trial balance** — always a derived view (`roll_tb`), never an authored schedule of free totals.
- **Skill** — install surface (`SKILL.md`); may alias a legacy name while doctrine targets an intent.
