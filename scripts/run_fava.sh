#!/usr/bin/env bash
# Launch Fava (Beancount web UI) on a ledger file.
# Usage:
#   scripts/run_fava.sh path/to/main.beancount
#   scripts/run_fava.sh path/to/main.beancount --port 5001
set -euo pipefail

LEDGER="${1:-}"
if [[ -z "$LEDGER" || ! -f "$LEDGER" ]]; then
  echo "Usage: $0 path/to/main.beancount [--port N] [extra fava args...]"
  exit 1
fi
shift || true

PORT=5000
EXTRA=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)
      PORT="${2:?}"
      shift 2
      ;;
    *)
      EXTRA+=("$1")
      shift
      ;;
  esac
done

FAVA_BIN="$(command -v fava || true)"
if [[ -z "$FAVA_BIN" ]]; then
  for c in "$HOME/Library/Python/3.12/bin/fava" "$HOME/.local/bin/fava"; do
    if [[ -x "$c" ]]; then FAVA_BIN="$c"; break; fi
  done
fi
if [[ -z "$FAVA_BIN" ]]; then
  echo "ERROR: fava not found. Install: pip install fava beancount"
  exit 2
fi

# Optional check
if command -v bean-check >/dev/null 2>&1; then
  bean-check "$LEDGER" || { echo "bean-check failed; fix ledger before Fava"; exit 1; }
elif [[ -x "$HOME/Library/Python/3.12/bin/bean-check" ]]; then
  "$HOME/Library/Python/3.12/bin/bean-check" "$LEDGER" || exit 1
fi

echo "Opening Fava on http://127.0.0.1:${PORT}"
echo "Ledger: $LEDGER"
echo "Stop with Ctrl+C"
exec "$FAVA_BIN" --host 127.0.0.1 --port "$PORT" "$LEDGER" "${EXTRA[@]+"${EXTRA[@]}"}"
