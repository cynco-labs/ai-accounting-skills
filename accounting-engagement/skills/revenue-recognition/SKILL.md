---
name: revenue-recognition
description: Revenue recognition analysis under MPERS/MFRS for material money in. Use when revenue recognition, sales cut-off, deferred revenue, principal vs agent.
disable-model-invocation: true
---
# /revenue-recognition

## Purpose

Thin alias into **classify** — revenue theme only.  
Same doctrine: `shared/classify-substance.md`.  
Same output folder: `workpapers/analysis/revenue_recognition.md`.

## Steps

1. Ensure `workpapers/transactions.json` exists (run **extract** if not).  
2. Set `classify_depth` = `standards_aware` for this theme.  
3. Load `references/jurisdictions/malaysia/standards/revenue_recognition.md` (or active jurisdiction pack).  
4. Follow **classify-transactions** steps 1–3 focused on material credits / sales streams.  
5. Write `workpapers/analysis/revenue_recognition.md` from `references/schemas/analysis_pack.example.md`.  
6. Apply concluded COA codes; update `payee_map.json`; re-run classify script for affected lines.

**Done when:** revenue pack on disk with sources, standard ref, conclusion → codes; open items listed.

## Do not

- Invent a second pipeline  
- Code all bank credits as sales without substance  
- Skip structured asks when recognition date is ambiguous  
