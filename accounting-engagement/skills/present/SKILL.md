---
name: present
description: >
  Human pack (HTML board) plus statements when depth needs them. Use when
  presenting books, opening the pack, or drafting FS/notes from adjusted TB.
disable-model-invocation: true
---
# /present

**Default human handoff = HTML board**, not markdown files.

Doctrine: `shared/html-deliverables.md` · truth order: JSON/TB → Beancount (ledger) → Fava (viewer only).

## Do this

### Always (any depth)

```bash
python3 scripts/generate_html_report.py clients/<slug>
# → outputs/<slug>_pack.html
```

1. Refresh HTML after TB / answers.  
2. Tell the user: **open that file** (actions · proof · books · matches).  
3. Do **not** hand off `README.md` / `queries.md` / TB `.md` as the deliverable.

### When depth needs statements (`year_end` / compilation / user asked FS)

4. Run **`prepare-primary-statements`** (numbers from adjusted TB only).  
5. Notes if needed: **`prepare-notes`**.  
6. Optional: workbook / compilation report.  
7. Refresh HTML again.

**Done when:** `outputs/<slug>_pack.html` exists and is fresh vs TB; primaries/notes only if in scope.

See `shared/slash-surface.md`.
