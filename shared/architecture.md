# End-to-end flow

**Core rules:** `shared/kernel-contract.md` · **six main jobs:** `shared/skill-collapse-map.md` · **plain English:** `CONTEXT.md`.

```text
┌─────────────────────────────────────────────────────────────┐
│  USER FOLDER (banks / receipts / “do the accounts”)         │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌──────────────────┐   do the books (smart intake, ≤3 questions)
│ engagement state │◄── engagement_state.json on disk
└────────┬─────────┘
         ▼
┌──────────────────────────────────────────┐
│ EXTRACT   extract_bank.py                │
│ CLASSIFY  classify_transactions.py       │
│ POST      post_journals.py               │
│ BUILD TB  roll_tb.py   ◄─ never hand-type│
│ RECON     bank RM0 (must pass)           │
│ YE        journals_ye.json → adjusted TB │
│ PRESENT   FS / notes from adjusted TB    │
│ PROVE     close_engagement.py            │
└────────────────────┬─────────────────────┘
                     ▼
┌──────────────────────────────────────────┐
│ LOCKED    approval recorded              │
│ BEANCOUNT ledger/main.beancount  ◄─ main │
│ FAVA      http://127.0.0.1:5000   ◄─ UI  │
│ TAX       from locked figures            │
└──────────────────────────────────────────┘
```

## CLI commands (in order)

```bash
extract → classify → post → tb → close → ledger
```

## Working files vs deliverables

| File | Role |
|---|---|
| `workpapers/*.json` | Machine-readable workpapers mid-job |
| `outputs/workpapers.xlsx` | Human working papers (Excel) |
| `outputs/fs/*` | Draft / final financial statement packs |
| **`ledger/main.beancount`** | **Official double-entry ledger** |
| Fava | Browser view of Beancount |

## Non-negotiables

- No made-up numbers  
- Bank recon and TB must balance (or clear **with limitation** note)  
- Files on disk over chat memory  
- **TB only via `roll_tb.py`**  
- Beancount only after journals balance (`bean-check`)  
