# Managed-agent cookbooks

Templates for **scheduled or headless** accounting workflows. Same skills and guardrails as interactive plugins; different runtime (cron, queue, orchestrator).

## Cookbooks

| Cookbook | Purpose | Default cadence |
|---|---|---|
| [filing-deadline-watcher](./filing-deadline-watcher/) | Digest of upcoming tax/statutory deadlines for active clients | Weekly |
| [bank-statement-intake](./bank-statement-intake/) | Detect new bank statement drops and stage them for bookkeeping | Daily / on folder event |

## Security tiers

| Tier | Meaning |
|---|---|
| **Read-only** | Reads client folders + writes digests/logs only |
| **Prepare** | Can draft journals/workpapers; cannot mark final or send externally |
| **Act** | Reserved — requires explicit firm enablement; not shipped default-on |

All cookbooks in this repo ship as **Read-only** or **Prepare**.

## Deployment notes

- Point the agent at firm config: `~/.claude/plugins/config/claude-for-accounting/`
- Restrict filesystem to client workspace roots
- Never enable unsupervised external send
- Tag all statutory dates `[verify]`

## Adding a cookbook

1. Create `managed-agent-cookbooks/<slug>/`
2. Include `README.md`, `agent.yaml` (or host-equivalent), and optional subagent specs
3. Reference existing skills by path — do not duplicate doctrine
4. Document security tier and failure modes
5. List in this README
