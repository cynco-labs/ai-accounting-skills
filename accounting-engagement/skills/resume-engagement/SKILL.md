---
name: resume-engagement
description: >
  Resume from engagement_state.json. Use when continue client, pick up
  books, or where we left off.
---

# /resume-engagement

## Purpose

Make multi-session work safe. **Disk is truth.**

## Workflow

1. Find `engagement_state.json`:
 - cwd, or
 - cwd/clients/*/engagement_state.json, or
 - path user provides, or
 - fixtures path if testing
2. Load state + `shared/agent-runtime.md` + `shared/operator-lens.md` + `references/stage_artifacts.md`
3. If `operator` missing → resolve once and write it (do not re-ask if inferable)
4. Verify artifacts listed in `state.artifacts` still exist
5. Run `python3 scripts/validate_engagement_artifacts.py <client_dir>` if workpapers present
6. Print status board:

```markdown
## Resume — [legal_name] · [operator] · [engagement_type] · period [fy / on-disk]
- Stage: [current_stage] ([status])
- Completed: [stages_completed]
- Blockers: [blockers or none]
- Open queries: [n]
- Next: [concrete next skill/action]
```

7. If `status == blocked` → work the blocker first 
8. If `status == waiting_on_user` and `open_queries` non-empty → 
 re-issue unanswered asks via **structured user-question tool** 
 (`shared/user-questions.md`) — do not only re-print `queries.md` 
9. Else continue from `current_stage` by loading that stage’s SKILL.md 
10. Do **not** restart the pipeline from setup unless user says so

## If no state file

Say so clearly. Offer:

- `engagement-setup` for a new client 
- `full-engagement-pipeline` if they dumped files

## Completion

**Done when:** state loaded, one-line status shown, next stage skill identified (or blockers listed).

