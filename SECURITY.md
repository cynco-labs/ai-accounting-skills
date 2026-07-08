# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `1.x` (main branch) | ✅ |
| Pre-1.0 experimental forks | ❌ — upgrade to main |

## What this project is

Markdown skills and optional Python scripts that run **inside the user’s agent environment**. They can instruct the agent to read client files the user points at. Treat installed skills as **code that influences access to sensitive financial data**.

## Reporting a vulnerability

Please **do not** open a public issue for:

- Prompt-injection patterns in skills that exfiltrate data
- Scripts that execute unsafe shell by default
- Secrets accidentally committed to the repo
- Ways to bypass mathematical or finalisation gates in a way that could mislead non-experts

Prefer private disclosure via GitHub Security Advisories on the repository, or email the addresses listed in `MAINTAINERS.md` once published.

Include:

1. Affected plugin/skill path  
2. Description of the behavior  
3. Impact (data exfiltration, silent imbalance, etc.)  
4. Minimal reproduction  

We aim to acknowledge within 7 days and ship fixes as soon as practical.

## Security expectations for contributors

- No credentials, API keys, or client data in the repo  
- Community skills must go through `accounting-builder-hub:skills-qa` before recommendation  
- `scripts/` must not download and execute remote code  
- Hooks, if added, must be documented and least-privilege  

## User responsibilities

- Install plugins from sources you trust  
- Prefer user-scoped installs you control  
- Never paste production secrets into chat logs you don’t control  
- Review draft financial statements before any external issuance  
