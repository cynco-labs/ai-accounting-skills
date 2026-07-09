#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Ensure VERSION and package.json version stay in lockstep.

Usage:
  python3 scripts/version_check.py
  python3 scripts/version_check.py --print   # print version only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", action="store_true", help="Print package version and exit 0")
    args = ap.parse_args()

    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    pkg_ver = str(pkg.get("version") or "").strip()
    file_ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    if args.print:
        print(pkg_ver)
        return 0

    errors: list[str] = []
    if not pkg_ver:
        errors.append("package.json missing version")
    if not file_ver:
        errors.append("VERSION file empty")
    if pkg_ver and file_ver and pkg_ver != file_ver:
        errors.append(f"version mismatch: package.json={pkg_ver!r} VERSION={file_ver!r}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"OK: version {pkg_ver}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
