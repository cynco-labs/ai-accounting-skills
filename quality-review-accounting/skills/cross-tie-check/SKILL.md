---
name: cross-tie-check
description: >
  Perform focused cross-tie tests: notes to primaries, cash flow to BS, profit to equity, opening balances to prior year signed FS, and internal cross-references.
---

# /cross-tie-check

## Purpose

Deep consistency after statements + notes exist.

## Tests
1. Assets = L + E  
2. Cash flow net change = Δ cash on SOFP  
3. Profit = RE movement (adjust for dividends/other equity)  
4. Opening balances = prior year signed FS closing  
5. Each note total = primary line  
6. Cross-reference numbers (Note X on face) correct  
7. Related party balances ⊆ AR/AP/loan notes  
8. Tax expense note ↔ tax computation ↔ tax payable  

## Output
Tie schedule with differences (must be zero or explained).
