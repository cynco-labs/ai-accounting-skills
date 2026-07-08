#!/usr/bin/env bash
# Production CI / local pre-PR check for ai-accounting-skills
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== validate_marketplace =="
python3 scripts/validate_marketplace.py

echo "== umbrella sync (source-of-truth drift) =="
python3 scripts/sync_umbrella.py --check

echo "== golden engagement artifacts =="
python3 scripts/validate_engagement_artifacts.py fixtures/golden-mini-sdn-bhd

echo "== stage gates =="
python3 scripts/validate_stage_gates.py fixtures/golden-mini-sdn-bhd

echo "== unit tests =="
python3 -m unittest discover -s tests -v

echo "== utterance routing evals =="
python3 scripts/eval_utterance_routing.py --top-k 3

echo "== close proof (golden) =="
python3 scripts/close_engagement.py fixtures/golden-mini-sdn-bhd --no-export-ledger

if [[ -f fixtures/golden-mini-sdn-bhd/ledger/main.beancount ]]; then
  echo "== bean-check golden ledger =="
  if command -v bean-check >/dev/null 2>&1; then
    bean-check fixtures/golden-mini-sdn-bhd/ledger/main.beancount
  elif [[ -x "$HOME/Library/Python/3.12/bin/bean-check" ]]; then
    "$HOME/Library/Python/3.12/bin/bean-check" fixtures/golden-mini-sdn-bhd/ledger/main.beancount
  else
    echo "WARN: bean-check not installed — skip (pip install beancount)"
  fi
fi

echo "OK: all ci_check steps passed"
