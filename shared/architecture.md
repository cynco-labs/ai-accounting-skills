# End-to-end architecture

```text
┌─────────────────────────────────────────────────────────────┐
│  USER DUMP (folder of banks / receipts / “do the accounts”) │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌──────────────────┐   smart-intake (infer, ≤3 questions)
│ engagement state │◄── engagement_state.json on disk
└────────┬─────────┘
         ▼
┌──────────────────────────────────────────┐
│ EXTRACT  pdfplumber / CSV                │
│   → transactions.json                    │
│   → optional bank xlsx (openpyxl)        │
└────────────────────┬─────────────────────┘
                     ▼
┌──────────────────────────────────────────┐
│ BOOKKEEP  classify → journals.json       │
│ RECON     bank RM0 · subledgers          │
│ TB        preliminary                    │
│ YE        adjustments → ATB              │
│ MPERS     technical review               │
│ FS        primaries + notes              │
│ QC        Section A blockers             │
└────────────────────┬─────────────────────┘
                     ▼
┌──────────────────────────────────────────┐
│ FINALISE  lock numbers                   │
│ BEANCOUNT ledger/main.beancount  ◄─ SoR  │
│ FAVA      http://127.0.0.1:5000   ◄─ UI  │
│ TAX       from locked figures            │
└──────────────────────────────────────────┘
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
- Beancount only after journals balance (`bean-check`)  
