# Words we use (plain English)

Short glossary for humans and agents. Prefer these words in skills, tickets, and chat.

**Throw-work first read:** `shared/runtime-brief.md` (one screen).  
Mechanics: `shared/kernel-contract.md` · six jobs: `shared/skill-collapse-map.md` · shelf: `shared/shelf-first.md` · craft: `shared/skill-craft.md`.

---

## Everyday terms

**Client job / engagement**  
One client + one period (or financial year) we are working on. Lives in a folder with `engagement_state.json`.  
_Also ok:_ engagement (firms already use this).  
_Avoid:_ “kernel run”, “pipeline invocation”

**Shelf (the papers)**  
Standard client folder layout under `clients/<slug>/` with sources sorted (`source/bank`, …) and a register.  
Docs may arrive from cwd, Desktop, or many paths — **organize first**, then extract.  
Doctrine: `shared/shelf-first.md`.  
_Avoid:_ booking from a random pile with no client folder

**Job map**  
When a dump has more than one company (or year), the short table of entity · period · docs · confidence before opening a shelf.  
_Avoid:_ mixing two companies into one set of workpapers

**Six main jobs**  
The product in six plain steps — also the **short slash commands** users type:

| Job | Slash | Meaning |
|---|---|---|
| **Do the books** | `/do-books` | Start or continue the whole job |
| **Extract** | `/extract` | Pull bank (and other) lines into a clean file |
| **Classify** | `/classify` | Understand the money (standards-aware) then put lines on COA codes |
| **Post** | `/post` | Double-entry journals; **trial balance is calculated** |
| **Present** | `/present` | Financial statements, notes, Excel, tax schedules |
| **Prove** | `/prove` | QC, lock, export the official ledger |

Front door: **“do the accounting”** or `/do-books`. Optional menu: `/ask-accounting` (if lost).  
Menu design: `shared/slash-surface.md`. Long skill names still exist for the model.

**Operator (who is driving)**  
Same engine for everyone. Stored as `operator` on `engagement_state.json`:

| Value | Meaning |
|---|---|
| **owner** | Doing their own books |
| **bookkeeper** | Bookkeeper for this entity |
| **firm** | Practice staff on a client job |

**Depth** is separate: `engagement_type` + `classify_depth` (how far we go).  
Doctrine: `shared/operator-lens.md`. **Do not** split into business vs firm slash products.

**Core tools / scripts**  
The programs that do the math the same way every time: extract → classify → post → build TB → close / export.  
_Avoid:_ “kernel”, “pure functions” in user-facing text  
_In code paths:_ file names like `kernel-contract.md` may still appear — treat them as **core rules**.

**Standard work files**  
Named files that hold amounts or lines, e.g. `transactions.json`, `journals.json`, `tb_*.json`, `ledger/main.beancount`.  
Judgment memos live under `workpapers/analysis/` (not TB totals).  
_Avoid:_ “truth shapes”, “artifacts” without the file name

**Classify depth**  
- **bookkeeping** — script + review queue; fast  
- **standards_aware** — substance under the framework for material themes, write analysis packs, then codes  
Doctrine: `shared/classify-substance.md`.

**Build the TB (roll_tb)**  
Trial balance comes only from journals via `scripts/roll_tb.py` (or `npx … tb`). **Never type TB totals by hand.**  
_Avoid:_ “prepare a TB in Excel first as the source of truth”

**Work the months you have**  
If the client only gave some months, book those months properly. Don’t stall for twelve months. Full-year FS only when coverage is enough (or the user accepts a clear limitation).  
_Avoid:_ “period-first doctrine” in client chat

**Files are the books**  
What is saved on disk beats chat memory. After a long session or a break, re-read the files.  
_Avoid:_ “disk is truth” in client-facing notes (use plain sentence above)

**Must stop (hard stop)**  
A check that failed so badly we cannot call the work final (e.g. TB does not balance). Stop and fix or escalate.  
_In state files you may still see:_ `blocker`  
_Avoid:_ calling a hard stop a “warning” only

**With limitation**  
We continue the work, but we clearly note what is incomplete (e.g. missing bank months for full-year FS).  
_In state files you may still see:_ `AMBER`  
_Avoid:_ hiding the limitation

**Source of the figure**  
Where a material number came from: bank statement page, prior signed FS, or a formula on those. Tag it.  
_Avoid:_ “provenance” in client emails; say “source” instead

**Clear question (≤3)**  
When we must ask the user something that blocks progress: use the agent’s question UI if available, max 3 questions, with options, recommended answer first. See `shared/user-questions.md`.

**Status board**  
Short update after progress: what stage, what’s stuck, what’s next.  
_Avoid:_ dumping slash-command names at clients

**Country pack**  
Tax / entity / reporting rules as data under `references/jurisdictions/<id>/`, not a forked copy of every skill.  
_Avoid:_ “jurisdiction pack” if “country pack” is clearer in chat

**Firm profile**  
Your firm’s name and defaults from setup — not hard-coded into the open-source repo.

---

## How they fit together

- A **client job** moves through the **six main jobs**; each job reads/writes **standard work files**.
- **Scripts** build the trial balance and postings; people (and the agent with judgment) choose codes and year-end adjustments — they do **not** invent TB totals.
- A **must stop** blocks finalising; a **with limitation** note lets bookkeeping continue under partial coverage.

---

## Easy mix-ups

- **Stage name** in `engagement_state.json` (many fine steps) vs **six main jobs** (product surface).
- **Trial balance** — always **calculated** from journals, never a free-typed schedule that “becomes” the truth.
- **Skill name** on disk may be an old alias; the job it serves is one of the six.
