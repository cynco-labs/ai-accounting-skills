---
name: tax-computation
description: >
 Malaysian tax computation from accounts (present job). Use when Form C, tax
 comp, or chargeable income.
---
# /tax-computation

## Purpose

ITA 1967 computation from accounting profit.

## Preconditions

1. Read shared guardrails (`shared/guardrails.md`).
2. Load firm profile from `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` if present.
3. Load plugin config from `~/.claude/plugins/config/claude-for-accounting/{{plugin}}/CLAUDE.md` if present.
4. Load active client engagement README / workspace if one is open.
5. **Never fabricate numbers.** Re-read source documents if figures are missing from context.



Load `references/tax_malaysia.md`.

## Prefer locked FS numbers
If FS not locked, tag computation `[DRAFT — subject to final accounts]`.

## Steps
1. Start from accounting profit/(loss) before tax 
2. Add-backs (non-deductible) 
3. Deductions (non-taxable income removed, allowable items) 
4. Capital allowances (IA/AA) — or call `capital-allowances` skill 
5. Apply losses b/f rules 
6. Chargeable income 
7. Apply correct rate schedule for entity 
8. Tax charged vs CP204/CP500 instalments → payable/(repayable) 
9. Deferred tax bridge if FS recognises deferred tax 


## Completion

**Done when:** tax schedule on disk from locked (or [DRAFT]) figures; rates from reference with [verify] where needed.

## Output
Tax computation schedule + journal for tax provision if YE skill needs update. 
**Never invent CA rates or tax rates** — use reference file; if outdated, flag verify against current IRB/LHDN.
