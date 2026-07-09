---
name: ask-accounting
description: Optional router if lost — which slash to use. Prefer saying do the accounting.
disable-model-invocation: true
---
# /ask-accounting

## Purpose

**Optional.** For users who are lost and want a menu.  

Default path is **not** this skill — say **“do the accounting”** or `/do-books` and go.

Do **not** run the whole engagement here. Recommend **one** short command; if they say “go”, run it.

## Load

`shared/slash-surface.md` · `shared/runtime-brief.md`

## Map (recommend one)

| Situation | Recommend |
|---|---|
| Folder dump / “do the accounting” / unknown company | **do-books** (just run it) |
| Continue mid-job | **resume** or **do-books** |
| Only parse banks | **extract** |
| Classifications / revenue / capex | **classify** (or **revenue** / **capex**) |
| Post / TB | **post** |
| FS / notes | **present** |
| QC / lock | **prove** |
| Firm first install only | `cold-start-interview` |
| Tax only | `tax-computation` |

## Output format

```markdown
**Recommended:** /do-books
**Why:** …
**Or just say:** “do the accounting” and I’ll run it.
```

**Done when:** one clear recommendation; user can say “run it” without learning the whole menu.
