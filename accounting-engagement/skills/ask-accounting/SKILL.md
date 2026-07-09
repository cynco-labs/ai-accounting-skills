---
name: ask-accounting
description: Router — which accounting skill or slash to use for this situation.
disable-model-invocation: true
---
# /ask-accounting

## Purpose

One place to remember. Map the user’s situation to a **short command** from `shared/slash-surface.md`.

Do **not** run the whole engagement here. Recommend, then wait for confirmation (or run the chosen skill if they say “go”).

## Load

`shared/slash-surface.md` · `shared/skill-collapse-map.md` · `CONTEXT.md`

## Map (recommend one)

| Situation | Recommend |
|---|---|
| Folder dump / “do the accounting” / unknown company | **do-books** |
| Continue mid-job / left off yesterday | **resume** |
| Only parse banks / Maybank PDF | **extract** |
| Code lines / classifications / revenue recognition / capex | **classify** (or **revenue** / **capex** if only that theme) |
| Post journals / trial balance | **post** |
| Draft balance sheet / P&L / notes | **present** |
| QC / partner review / lock | **prove** |
| Firm first install (not client dump) | `cold-start-interview` (long name OK) |
| Tax computation only | `tax-computation` |

## Output format

```markdown
**Recommended:** /do-books (or /accounting-engagement:do-books on Claude plugins)

**Why:** …

**Next after that:** …

**Optional branches:** …
```

**Done when:** one clear recommendation + why; user knows what to type or can say “run it”.
