#!/usr/bin/env bash
# SessionStart: if engagement_state.json exists nearby, inject resume context.
set -euo pipefail

ROOT_PLUGIN="${CLAUDE_PLUGIN_ROOT:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Prefer plugin script; fall back to monorepo scripts when developing from source
SCANNER=""
if [[ -n "$ROOT_PLUGIN" && -f "$ROOT_PLUGIN/hooks-handlers/find_engagement_state.py" ]]; then
  SCANNER="$ROOT_PLUGIN/hooks-handlers/find_engagement_state.py"
elif [[ -f "$SCRIPT_DIR/find_engagement_state.py" ]]; then
  SCANNER="$SCRIPT_DIR/find_engagement_state.py"
else
  # monorepo checkout: plugin root may be engagement-accounting/
  MONO="$(cd "$SCRIPT_DIR/../.." && pwd)"
  if [[ -f "$MONO/engagement-accounting/hooks-handlers/find_engagement_state.py" ]]; then
    SCANNER="$MONO/engagement-accounting/hooks-handlers/find_engagement_state.py"
  fi
fi

if [[ -z "$SCANNER" ]]; then
  exit 0
fi

CONTEXT="$(python3 "$SCANNER" 2>/dev/null || true)"
if [[ -z "$CONTEXT" ]]; then
  exit 0
fi

# JSON-escape the context for the hook payload
python3 - "$CONTEXT" <<'PY'
import json, sys
context = sys.argv[1]
payload = {
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": context,
  }
}
print(json.dumps(payload))
PY

exit 0
