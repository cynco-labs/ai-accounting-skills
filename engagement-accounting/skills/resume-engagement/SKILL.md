---
name: resume-engagement
description: >
  Resume an in-progress accounting engagement from engagement_state.json and
  artifacts on disk. Trigger on resume, continue client, "where were we", pick
  up year end, session start with existing client folder, engagement_state
  present. Reads disk only — never reconstructs numbers from chat memory.
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
2. Load state + `shared/agent-runtime.md` + `references/stage_artifacts.md`
3. Verify artifacts listed in `state.artifacts` still exist
4. Run `python3 scripts/validate_engagement_artifacts.py <client_dir>` if workpapers present
5. Print status board:

```markdown
## Resume — [legal_name] FYE [fy_end]
- Stage: [current_stage] ([status])
- Completed: [stages_completed]
- Blockers: [blockers or none]
- Open queries: [n]
- Next: [concrete next skill/action]
```

6. If `status == blocked` → work the blocker first  
7. Else continue from `current_stage` by loading that stage’s SKILL.md  
8. Do **not** restart the pipeline from setup unless user says so  

## If no state file

Say so clearly. Offer:

- `engagement-setup` for a new client  
- `full-engagement-pipeline` if they dumped files  
