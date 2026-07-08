#!/usr/bin/env bash
# Install every claude-for-accounting plugin (modular path).
# Prefer the umbrella for throw-work agents:
#   /plugin install accounting-engagement@claude-for-accounting
set -euo pipefail

MARKETPLACE="${1:-claude-for-accounting}"

PLUGINS=(
  accounting-engagement
  engagement-accounting
  bookkeeping-accounting
  reconciliation-accounting
  year-end-accounting
  mpers-accounting
  financial-statements-accounting
  quality-review-accounting
  finalisation-accounting
  tax-accounting
  beancount-ledger
  accounting-builder-hub
)

echo "Install these in Claude Code (user scope recommended):"
echo
echo "  /plugin marketplace add <path-or-url-to-this-repo>"
echo
for p in "${PLUGINS[@]}"; do
  echo "  /plugin install ${p}@${MARKETPLACE}"
done
echo
echo "Minimal throw-work install (recommended):"
echo "  /plugin install accounting-engagement@${MARKETPLACE}"
echo "  /plugin install accounting-builder-hub@${MARKETPLACE}   # optional, contributors"
echo
echo "Then restart Claude Code and run:"
echo "  /accounting-engagement:cold-start-interview"
echo "  # or dump a client folder and ask to do the year end"
