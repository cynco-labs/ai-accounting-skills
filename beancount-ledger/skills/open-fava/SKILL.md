---
name: open-fava
description: >
  Open Fava UI on a valid Beancount ledger. Use when fava, browse books,
  or interactive P&L.
---

# /open-fava

## Purpose

**Fava** is the impressive UI on top of Beancount — local browser, not Excel.

```text
ledger/main.beancount → fava → http://127.0.0.1:5000
```

## Preconditions

1. Ledger exists (`export-beancount` first if not) 
2. `bean-check` PASS (run validate skill) 
3. `fava` installed: `pip install fava beancount`

## Command

```bash
scripts/run_fava.sh path/to/main.beancount
# custom port
scripts/run_fava.sh path/to/main.beancount --port 5001
```

Or:

```bash
fava --host 127.0.0.1 --port 5000 path/to/main.beancount
```

## Agent behavior

1. Validate ledger first 
2. Start Fava **in background** if the host supports long-running processes 
3. Tell the user the URL: `http://127.0.0.1:5000` 
4. Default bind **localhost only** — do not expose `0.0.0.0` unless user asks 
5. If fava missing: print install one-liner; do not pretend UI is open 

## What to show the user

- Income Statement / Balance Sheet in Fava 
- Account tree 
- Journal entries from export 


## Completion

**Done when:** bean-check PASS, Fava started (or install instructions), user given localhost URL.

## Security

Client financial data stays local. No public tunnel unless explicitly requested.
