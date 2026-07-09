# End-to-end architecture

**First principles:** `shared/kernel-contract.md` · skill collapse: `shared/skill-collapse-map.md`.

```text
┌─────────────────────────────────────────────────────────────┐
│  USER DUMP (folder of banks / receipts / “do the accounts”) │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌──────────────────┐   do-books (smart-intake, ≤3 questions)
│ engagement state │◄── engagement_state.json on disk
└────────┬─────────┘
         ▼
┌──────────────────────────────────────────┐
│ EXTRACT   extract_bank.py                │
│ CLASSIFY  classify_transactions.py       │
│ POST      post_journals.py               │
│ ROLL TB   roll_tb.py   ◄─ never freestyle│
│ RECON     bank RM0 (gate)                │
│ YE        journals_ye.json → roll ATB     │
│ PRESENT   FS / notes from ATB map         │
│ PROVE     close_engagement.py            │
└────────────────────┬─────────────────────┘
                     ▼
┌──────────────────────────────────────────┐
│ LOCKED    approval recorded              │
│ BEANCOUNT ledger/main.beancount  ◄─ SoR  │
│ FAVA      http://127.0.0.1:5000   ◄─ UI  │
│ TAX       from locked figures            │
└──────────────────────────────────────────┘
```

## Kernel verbs (CLI)

```bash
extract → classify → post → tb → close → ledger
```

## Systems of record vs deliverables

| Artifact | Role |
|---|---|
| `workpapers/*.json` | Machine engagement state / intermediate truth |
| `outputs/workpapers.xlsx` | Human working papers (openpyxl) |
| `outputs/fs/*` | Draft / final FS packs |
| **`ledger/main.beancount`** | **Double-entry system of record** |
| Fava | Interactive view of Beancount |

## Non-negotiables

- No fabricated numbers  
- Bank recon and TB must balance (or documented limitation)  
- Disk artifacts over chat memory  
- **TB only via `roll_tb.py`**  
- Beancount only after journals balance (`bean-check`)  
