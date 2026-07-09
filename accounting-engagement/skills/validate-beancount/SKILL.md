---
name: validate-beancount
description: >
  Validate a Beancount ledger with bean-check. Use when bean-check or
  ledger broken.
---

# /validate-beancount

## Purpose

Prove the ledger file is valid before Fava or handoff.

## Command

```bash
bean-check path/to/main.beancount
# or
python3 -c "import subprocess; subprocess.check_call(['bean-check','path/to/main.beancount'])"
```

If `bean-check` missing:

```bash
pip install beancount
```

## Also check

1. File non-empty; has `option "operating_currency"`  
2. Has at least one `open` and one `*` transaction  
3. Engagement currency matches option  
4. Report path + PASS/FAIL clearly  

## On FAIL

Do not open Fava as “ready.” Fix export or journals and re-export.

## Completion

**Done when:** bean-check PASS/FAIL reported clearly; on FAIL do not treat ledger as ready.

