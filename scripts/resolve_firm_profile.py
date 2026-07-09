#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Resolve or scaffold multi-agent firm profile paths.

Usage:
  python3 scripts/resolve_firm_profile.py
  python3 scripts/resolve_firm_profile.py --init "Hazli & Co"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# allow running as script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_paths import firm_config_dir, firm_profile_candidates, resolve_firm_profile  # noqa: E402

TEMPLATE = """# Firm profile

> Multi-agent path. Prefer `~/.config/ai-accounting/firm-profile.md`.
> Legacy Claude path still works: `~/.claude/plugins/config/claude-for-accounting/firm-profile.md`.

## Identity

- **Firm name:** {name}
- **Jurisdiction default:** Malaysia
- **Framework default:** MPERS
- **Currency default:** MYR
- **Contact:** 

## Working preferences

- Materiality (line): RM 100
- Bank recon tolerance: RM 0.00
- TB balance tolerance: RM 0.00
- Suspense policy: last resort only

## Classification overrides

Add firm-specific payee → account rules in each client `workpapers/payee_map.json`,
or extend `references/classification_patterns.json` for practice-wide patterns.

## Notes

- Never fabricate numbers.
- Drafts for partner / licensed accountant review only.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", metavar="FIRM_NAME", help="Create profile if missing")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    found = resolve_firm_profile()
    if args.init:
        dest_dir = firm_config_dir()
        dest = dest_dir / "firm-profile.md"
        if dest.is_file():
            print(f"exists: {dest}")
            return 0
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest.write_text(TEMPLATE.format(name=args.init), encoding="utf-8")
        print(f"created: {dest}")
        return 0

    if args.json:
        import json

        print(
            json.dumps(
                {
                    "resolved": str(found) if found else None,
                    "candidates": [str(p) for p in firm_profile_candidates()],
                    "preferred_write": str(firm_config_dir() / "firm-profile.md"),
                },
                indent=2,
            )
        )
        return 0

    print("Firm profile resolution (first existing wins)")
    print("")
    for i, p in enumerate(firm_profile_candidates(), 1):
        mark = "→" if found and p.resolve() == found else " "
        exists = "✓" if p.is_file() else "·"
        print(f"  {mark} {exists} {p}")
    print("")
    if found:
        print(f"resolved: {found}")
        return 0
    print("resolved: (none)")
    print(f"scaffold: python3 scripts/resolve_firm_profile.py --init \"Your Firm\"")
    print(f"writes to: {firm_config_dir() / 'firm-profile.md'}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
