# Shelf the papers — before any books

**First principle:** A bookkeeper does not code lines from a messy desktop.  
They **find the papers → sort by client and year → put them on the shelf → then work**.

Agents must do the same. **Organize before extract.**  
Never invent company names or years to force a folder; **read the files first**.

See: `shared/smart-intake.md` · `shared/operator-lens.md` · `shared/kernel-contract.md` · `CONTEXT.md`

---

## The real world (what users actually do)

| How work arrives | Agent must |
|---|---|
| `cd` into a folder of mixed PDFs | Inventory that folder |
| Paste / `@` paths from Desktop, Downloads, iCloud | Accept **many roots** as input |
| Already-neat `clients/acme/source/…` | Detect existing shelf; **do not re-scatter** |
| One zip / “everything in this drive” | Inventory, then propose shelves |
| Multi-company dump in one place | Split by entity **before** mixing numbers |

**Inputs can be anywhere. The books only live in a standard shelf.**

---

## Order of work (non-negotiable)

```text
1. DISCOVER   — list every path the user named + cwd + obvious siblings
2. CLUSTER    — group files by likely entity + period (from names + peek headers)
3. SHELF      — create clients/<slug>/ layout; place or pointer-link sources
4. REGISTER   — source/register.md + coverage matrix
5. INTAKE     — operator + depth + soft-confirm (≤3)
6. EXTRACT    — only from shelved source/**
7. CLASSIFY → POST → … (six jobs as usual)
```

**Forbidden:** extract/classify/post from random Desktop paths with no client shelf.  
**Allowed:** read Desktop/Downloads **during discover**; then copy or pointer into the shelf.

---

## Standard shelf (one client job)

Root is usually the workspace the user opened (or a path they chose).  
One job = **one entity + one period** under:

```text
clients/<slug>/
  README.md                 # decisions, inferences, open questions
  engagement_state.json     # operator, depth, stage — not balances
  source/
    register.md             # inventory + coverage (mandatory)
    inbox/                  # optional: unsorted arrivals this session
    bank/                   # statements (PDF/CSV)
    sales/                  # invoices, credit notes, POS
    purchases/              # supplier invoices
    payroll/                # payslips, EPF/SOCSO
    statutory/              # SSM, constitutions
    prior/                  # prior FS, TB, tax comp
    other/                  # tenancy, stock, misc
    _pointers.md            # optional: original paths when not copied
  workpapers/               # transactions, journals, TB, analysis, recon
  outputs/                  # FS, tax, xlsx packs
  ledger/                   # main.beancount after prove
  queries.md                # paper trail of asks
```

**Slug:** lowercase, hyphens, from legal name or folder (`acme-sdn-bhd`).  
**Period:** prefer `fy_end` year in README/state; multi-year clients get **one folder per job** or clear period in state — never mix two FYs in one `workpapers/`.

### Multi-client workspace

```text
{workspace}/
  clients/
    acme-sdn-bhd/     # job A
    beta-enterprise/  # job B
  PRACTICE.md         # optional firm note — not balances
```

When several entities appear in one dump:

1. Build a **Job map** (table: entity · period · file count · confidence).  
2. Soft-confirm which job(s) to open **now** (default: largest / clearest bank set).  
3. Shelf **each** chosen job separately. Never merge two companies’ lines.

---

## Discover (how to explore like a bookkeeper)

### 1. Collect input roots

Union of:

- Current working directory  
- Paths the user pasted / `@`-mentioned  
- If cwd is empty of docs: common siblings only if user pointed (“also check Downloads/…”) — **do not** silently scan the whole home directory  

### 2. Inventory (names first, then peek)

For each file (and shallow dirs):

| Capture | Why |
|---|---|
| Path, name, extension, size, mtime | Sort + dedupe |
| Kind guess | bank / invoice / payslip / statutory / prior FS / junk |
| Period guess from filename | `2025-03`, `Mar2025`, `FY2025` |
| Entity guess from filename / parent folder | `Acme`, `SDN BHD` |
| After peek (bank PDF/CSV header only) | Account title, bank brand, currency, statement dates |

Write a working list **before** moving files. Prefer `source/register.md` draft or `clients/_inbox/DISCOVER.md` if multi-job.

### 3. Kind heuristics (filename + light peek)

| Signals | Kind → shelf subfolder |
|---|---|
| Maybank, CIMB, RHB, statement, e-Statement, `*bank*`, `.csv` of bank export | `source/bank/` |
| Invoice, inv-, tax invoice, OR, receipt | `source/sales/` or `purchases/` (direction from context) |
| Payslip, EA, PCB, EPF, KWSP, SOCSO, EIS | `source/payroll/` |
| SSM, Form 9/13/24/44/49, constitution | `source/statutory/` |
| “Financial statements”, “FS 2024”, CT600/Form C, tax computation | `source/prior/` |
| Screenshot, meme, `.DS_Store`, random | **archive / ignore** — list under register “Not used” |

### 4. Cluster → jobs

```text
Cluster key ≈ (normalized entity name, year or period span)
```

- Same account title + contiguous months → one job  
- Two Sdn Bhd names in one folder → **two jobs**  
- Personal name + company name → ask once which is reporting entity  

---

## Place files on the shelf

| Strategy | When | How |
|---|---|---|
| **Copy into shelf** | Default for messy dumps | Copy into `source/<kind>/`; keep originals untouched |
| **Move into shelf** | User says “organize this folder” | Move; note in register |
| **Pointer only** | Huge files / user forbids copy | List path in `source/_pointers.md` + register; extract may read original path **if recorded** |
| **Already shelved** | Paths already under `clients/<slug>/source/` | Do not re-copy; refresh register only |

**Rules:**

1. Prefer **copy** over move unless user asked to tidy in place.  
2. Never delete user originals.  
3. Dedupe by hash or (name + size + mtime); keep one, list duplicates in register.  
4. Unreadable / password PDF → register as gap, not silent skip.  
5. After shelf: **all extract inputs are under that job’s `source/` or listed pointers.**

---

## Job map (show the user when multi-entity or messy)

```markdown
## What I found
| Job | Entity (guess) | Period | Banks | Other docs | Confidence |
|---|---|---|---|---|---|
| 1 | Acme Sdn. Bhd. | 2025-01→2025-11 | 11 | 4 invoices | high |
| 2 | Beta Enterprise | 2025 | 2 | — | medium |

## Shelf
- Creating `clients/acme-sdn-bhd/` for job 1 (recommended)
- Parking job 2 until you say so

## Next
- Soft-confirm entity + period
- Extract banks for job 1
```

One job clear → skip the table; still write the shelf.

---

## Register (`source/register.md`) minimum

1. **Input roots** examined  
2. **File table:** path (in shelf or pointer) · kind · period · notes  
3. **Coverage matrix:** bank months (and other types if material)  
4. **Not used / archive**  
5. **Readiness:** GREEN | AMBER | RED  
6. **Gaps** (numbered, plain language)

Then continue smart-intake (operator, depth, ≤3 asks) and extract.

---

## When to skip heavy re-shelf

| Situation | Action |
|---|---|
| Valid `engagement_state.json` + `source/register.md` | Resume; only add new files |
| User already used standard layout | Inventory + extract |
| Single clear bank PDF `@`-mentioned | Mini-shelf: create slug folder, put/copy that file under `source/bank/`, register, extract |

---

## Anti-patterns

| Don’t | Do |
|---|---|
| Extract from Desktop with no client folder | Shelf first |
| Mix two companies in one `transactions.json` | One job per shelf |
| Ask “what’s the company name?” before reading PDFs | Peek headers |
| Recursively scan entire home drive | Only roots user gave + cwd |
| Rename legal docs in place without a register | Register every placement |
| Start classify before register exists | Register → then extract → classify |

---

## Done when (shelf step)

- [ ] Input roots inventoried  
- [ ] Job map known (1+ jobs; active job chosen)  
- [ ] `clients/<slug>/` standard dirs exist  
- [ ] Sources copied/pointed under `source/**`  
- [ ] `source/register.md` written with coverage  
- [ ] Ready for smart-intake soft-confirm + extract  

**Not done:** pretty folders with no register, or books with no shelf.
