# Firm profile — multi-agent resolution

Agents must load firm defaults **before** inventing practice policy.

## Search order (first file wins)

1. `$AI_ACCOUNTING_FIRM_PROFILE` — explicit file path  
2. `$AI_ACCOUNTING_CONFIG/firm-profile.md`  
3. `$XDG_CONFIG_HOME/ai-accounting/firm-profile.md`  
4. `~/.config/ai-accounting/firm-profile.md` ← **preferred (all agents)**  
5. `./.ai-accounting/firm-profile.md` — project-local override  
6. `~/.claude/plugins/config/claude-for-accounting/firm-profile.md` — legacy Claude plugin path  

```bash
python3 scripts/resolve_firm_profile.py
python3 scripts/resolve_firm_profile.py --init "Your Firm Name"
```

## What belongs here

| Include | Exclude |
|---|---|
| Firm legal name, letterhead defaults | Client trial balances |
| **Default operator** (`firm` / `bookkeeper` / rarely `owner`) | Per-job balances (use `engagement_state`) |
| Default jurisdiction / framework / currency | Bank passwords |
| Materiality & recon tolerances | Fabricated sample numbers |
| Classification policy notes | Secrets / API keys |

Template: `shared/firm-profile-template.md`. Lens: `shared/operator-lens.md`.

## Agent instructions

1. Call the resolver (or walk the list above).  
2. If missing **and** work looks like practice/client work → offer cold-start / `--init` — do not invent a firm name.  
3. If missing **and** work looks like an owner folder dump → set `operator: owner` and continue without cold-start.  
4. Client workspaces remain under the engagement folder; firm profile is **practice-wide**.  
5. Never write client figures into the firm profile.

## Claude Code note

Claude plugins may still mirror config under `~/.claude/plugins/config/…`.  
That path remains valid; new installs should prefer `~/.config/ai-accounting/`.
