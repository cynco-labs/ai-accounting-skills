#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Sync stage-plugin skills into the accounting-engagement umbrella plugin.

Source of truth remains the modular stage plugins. The umbrella is a one-install
bundle for throw-work agents.

Usage:
  python3 scripts/sync_umbrella.py
  python3 scripts/sync_umbrella.py --check   # CI: fail if out of date
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UMBRELLA = ROOT / "accounting-engagement"
MANIFEST = UMBRELLA / "skills" / "SYNC_MANIFEST.json"

# (source plugin, skill dir name) — order is documentation only
STAGE_SKILLS = [
    ("engagement-accounting", "cold-start-interview"),
    ("engagement-accounting", "smart-intake"),
    ("engagement-accounting", "engagement-setup"),
    ("engagement-accounting", "source-documents"),
    ("engagement-accounting", "client-workspace"),
    ("engagement-accounting", "full-engagement-pipeline"),
    ("engagement-accounting", "resume-engagement"),
    ("bookkeeping-accounting", "extract-bank-statement"),
    ("bookkeeping-accounting", "record-transactions"),
    ("bookkeeping-accounting", "classify-transactions"),
    ("bookkeeping-accounting", "revenue-recognition"),
    ("bookkeeping-accounting", "capitalise-or-expense"),
    ("bookkeeping-accounting", "chart-of-accounts"),
    ("bookkeeping-accounting", "journal-entries"),
    ("reconciliation-accounting", "bank-reconciliation"),
    ("reconciliation-accounting", "subledger-reconciliations"),
    ("reconciliation-accounting", "preliminary-trial-balance"),
    ("year-end-accounting", "year-end-adjustments"),
    ("year-end-accounting", "adjusted-trial-balance"),
    ("mpers-accounting", "mpers-technical-review"),
    ("mpers-accounting", "disclosure-checklist"),
    ("financial-statements-accounting", "prepare-primary-statements"),
    ("financial-statements-accounting", "prepare-notes"),
    ("financial-statements-accounting", "compilation-report"),
    ("financial-statements-accounting", "generate-workbook"),
    ("quality-review-accounting", "quality-review"),
    ("quality-review-accounting", "cross-tie-check"),
    ("finalisation-accounting", "finalise-accounts"),
    ("finalisation-accounting", "management-approval"),
    ("finalisation-accounting", "auditor-pack"),
    ("finalisation-accounting", "statutory-handoff"),
    ("tax-accounting", "tax-computation"),
    ("tax-accounting", "capital-allowances"),
    ("beancount-ledger", "export-beancount"),
    ("beancount-ledger", "validate-beancount"),
    ("beancount-ledger", "open-fava"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def sync(check_only: bool) -> int:
    UMBRELLA.mkdir(parents=True, exist_ok=True)
    skills_root = UMBRELLA / "skills"
    skills_root.mkdir(exist_ok=True)

    manifest_entries = []
    mismatches = []

    for plugin, skill in STAGE_SKILLS:
        src = ROOT / plugin / "skills" / skill / "SKILL.md"
        if not src.is_file():
            print(f"ERROR: missing source skill {src}", file=sys.stderr)
            return 1
        dest_dir = skills_root / skill
        dest = dest_dir / "SKILL.md"
        digest = sha256_file(src)
        manifest_entries.append(
            {"plugin": plugin, "skill": skill, "sha256": digest, "source": str(src.relative_to(ROOT))}
        )

        if check_only:
            if not dest.is_file():
                mismatches.append(f"missing umbrella skill: {skill}")
            elif sha256_file(dest) != digest:
                mismatches.append(f"out of date: {skill}")
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        # Pure byte-identical copy so YAML frontmatter stays valid for the host.
        # Provenance lives in SYNC_MANIFEST.json — do not edit umbrella skills by hand.
        shutil.copy2(src, dest)

        # copy skill-local references if any
        src_refs = src.parent / "references"
        if src_refs.is_dir():
            dest_refs = dest_dir / "references"
            if dest_refs.exists():
                shutil.rmtree(dest_refs)
            shutil.copytree(src_refs, dest_refs)

    if check_only:
        if mismatches:
            for m in mismatches:
                print(f"ERROR: {m}")
            print("Run: python3 scripts/sync_umbrella.py", file=sys.stderr)
            return 1
        print(f"OK: umbrella in sync ({len(STAGE_SKILLS)} skills)")
        return 0

    MANIFEST.write_text(json.dumps({"skills": manifest_entries}, indent=2) + "\n", encoding="utf-8")

    # Remove stale umbrella skills not in manifest (except SYNC_MANIFEST)
    keep = {s for _, s in STAGE_SKILLS} | {"SYNC_MANIFEST.json"}
    for child in skills_root.iterdir():
        if child.is_dir() and child.name not in keep:
            shutil.rmtree(child)
            print(f"removed stale {child.name}")

    print(f"OK: synced {len(STAGE_SKILLS)} skills → accounting-engagement/skills/")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    return sync(check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
