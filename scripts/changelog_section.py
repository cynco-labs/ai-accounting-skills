#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Extract a Keep-a-Changelog section for GitHub release notes.

Usage:
  python3 scripts/changelog_section.py 2.2.2
  python3 scripts/changelog_section.py 2.2.2 --title-prefix "Release "
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract(changelog: str, version: str) -> str | None:
    # ## [2.2.2] — 2026-07-09  or  ## [2.2.2]
    pat = re.compile(
        rf"^## \[({re.escape(version)})\][^\n]*\n(.*?)(?=^## \[|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pat.search(changelog)
    if not m:
        return None
    body = m.group(2).strip()
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("version", help="Semver without leading v")
    ap.add_argument("--changelog", type=Path, default=ROOT / "CHANGELOG.md")
    args = ap.parse_args()

    text = args.changelog.read_text(encoding="utf-8")
    body = extract(text, args.version)
    if body is None:
        print(
            f"ERROR: no CHANGELOG section for [{args.version}]",
            file=sys.stderr,
        )
        return 1

    # GitHub release body
    out = f"""## What's new

{body}

## Install

```bash
npx skills add cynco-labs/ai-accounting-skills
npx @cynco/accounting-skills@{args.version} doctor
npx @cynco/accounting-skills@{args.version} close
```

## npm

[`@cynco/accounting-skills@{args.version}`](https://www.npmjs.com/package/@cynco/accounting-skills) — install with the version above.

## Notes

Drafts for professional accountant review only — not signed financial statements or tax advice.
"""
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
