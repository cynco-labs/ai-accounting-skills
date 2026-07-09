#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage gate checks — required artifacts before claiming a stage is done.

Depth-aware: uses references/depth_gates.json via depth_gates.py.
Does not invent progress. Only verifies claims already on disk.

Usage:
  python3 scripts/validate_stage_gates.py fixtures/golden-books-only-mini
  python3 scripts/validate_stage_gates.py fixtures/golden-mini-sdn-bhd --strict
  python3 scripts/validate_stage_gates.py ./clients/acme --require-atb
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from depth_gates import (  # noqa: E402
    check_journals,
    check_tb,
    print_scorecard,
    score_engagement,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("client_dir", type=Path)
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Require all gates for engagement_type (prove / done)",
    )
    ap.add_argument(
        "--soft",
        action="store_true",
        help="Only fail arithmetic / overclaims; missing progress is a warning",
    )
    ap.add_argument("--depth", help="Override engagement_type")
    ap.add_argument(
        "--require-atb",
        action="store_true",
        help="Fail if adjusted TB missing (forces year-end-style check)",
    )
    ap.add_argument("--require-ledger", action="store_true")
    args = ap.parse_args()
    client = args.client_dir.resolve()
    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    strict = True if args.strict else (False if args.soft else None)
    card = score_engagement(client, strict=strict, depth=args.depth)
    print_scorecard(card)

    # Legacy flags
    extra_errors: list[str] = []
    if args.require_atb and not (client / "workpapers/tb_adjusted.json").is_file():
        extra_errors.append("required gate missing: adjusted TB (--require-atb)")
    if args.require_ledger and not (client / "ledger/main.beancount").is_file():
        extra_errors.append("required gate missing: Beancount ledger (--require-ledger)")

    # Overclaim: stages_completed without files (legacy safety net)
    state = {}
    sp = client / "engagement_state.json"
    if sp.is_file():
        state = json.loads(sp.read_text(encoding="utf-8"))
    completed = set(state.get("stages_completed") or [])
    claim_map = {
        "source_documents": ["source/register.md"],
        "record_transactions": ["workpapers/transactions.json"],
        "journal_entries": ["workpapers/journals.json"],
        "preliminary_trial_balance": ["workpapers/tb_preliminary.json"],
        "year_end_adjustments": ["workpapers/journals_ye.json"],
        "adjusted_trial_balance": ["workpapers/tb_adjusted.json"],
        "quality_review": ["workpapers/qc_report.md"],
        "primary_statements": ["outputs/fs/primary_statements.md"],
        "notes": ["outputs/fs/notes.md"],
    }
    for stage, rels in claim_map.items():
        if stage in completed and not all((client / r).is_file() for r in rels):
            extra_errors.append(f"stages_completed has {stage} but missing {rels}")

    # Math on any present TB/journals even if optional for depth
    for rel, checker in [
        ("workpapers/tb_preliminary.json", check_tb),
        ("workpapers/tb_adjusted.json", check_tb),
        ("workpapers/journals.json", check_journals),
        ("workpapers/journals_ye.json", check_journals),
    ]:
        p = client / rel
        if p.is_file():
            ok, msg = checker(p)
            if not ok:
                extra_errors.append(f"{rel}: {msg}")

    for e in extra_errors:
        print(f"ERROR: {e}")
        card.errors.append(e)

    if card.errors or extra_errors:
        print(f"FAILED: {len(card.errors)} gate error(s)")
        return 1
    print(
        f"OK: stage gates depth={card.depth} "
        f"({sum(1 for r in card.results if r.ok)} checks ok, {len(card.warnings)} warning(s))"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
