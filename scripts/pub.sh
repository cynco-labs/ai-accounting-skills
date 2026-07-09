#!/usr/bin/env bash
# One-shot npm publish for this package (browser login may prompt — press ENTER).
set -euo pipefail
cd "$(dirname "$0")/.."
echo "Publishing @cynco/accounting-skills@$(cat VERSION)…"
echo "If npm asks: Press ENTER to open in the browser → do that, then sign in."
exec npm publish --access public
