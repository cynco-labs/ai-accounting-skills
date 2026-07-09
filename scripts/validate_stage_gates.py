#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Stage gate checks — required artifacts before claiming a stage is done.

Does not invent progress. Only verifies claims already on disk.

Usage:
  python3 scripts/validate_stage_gates.py fixtures/golden-mini-sdn-bhd
  python3 scripts/validate_stage_gates.py ./clients/acme --require-atb
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

TOL = Decimal("0.005")

# Logical pipeline order and hard prerequisites
GATES: list[tuple[str, list[str], str]] = [
    # (stage_id, required relative paths, human label)
    ("source_documents", ["source/register.md"], "source register"),
    ("record_transactions", ["workpapers/transactions.json"], "transactions"),
    ("journal_entries", ["workpapers/journals.json"], "journals"),
    ("preliminary_trial_balance", ["workpapers/tb_preliminary.json"], "preliminary TB"),
    ("year_end_adjustments", ["workpapers/journals_ye.json"], "YE journals"),
    ("adjusted_trial_balance", ["workpapers/tb_adjusted.json"], "adjusted TB"),
    ("quality_review", ["workpapers/qc_report.md"], "QC report"),
    ("finalise", ["workpapers/tb_adjusted.json"], "locked ATB"),
    ("beancount", ["ledger/main.beancount"], "Beancount ledger"),
]


def money(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def tb_balances(path: Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = data.get("lines") or []
    deb = sum((money(l.get("debit", 0)) for l in lines), Decimal("0"))
    cre = sum((money(l.get("credit", 0)) for l in lines), Decimal("0"))
    if abs(deb - cre) > TOL:
        return False, f"TB out of balance DR={deb} CR={cre}"
    return True, f"TB balanced DR={deb} CR={cre}"


def journals_balance(path: Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    bad = []
    for je in data.get("journals") or []:
        deb = sum((money(l.get("debit", 0)) for l in je.get("lines") or []), Decimal("0"))
        cre = sum((money(l.get("credit", 0)) for l in je.get("lines") or []), Decimal("0"))
        if abs(deb - cre) > TOL:
            bad.append(je.get("je_number", "?"))
    if bad:
        return False, f"unbalanced journals: {', '.join(bad)}"
    return True, f"{len(data.get('journals') or [])} journals balanced"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("client_dir", type=Path)
    ap.add_argument("--require-atb", action="store_true", help="Fail if adjusted TB missing")
    ap.add_argument("--require-ledger", action="store_true")
    args = ap.parse_args()
    client = args.client_dir.resolve()
    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    present: list[str] = []

    state = {}
    sp = client / "engagement_state.json"
    if sp.is_file():
        state = json.loads(sp.read_text(encoding="utf-8"))
    completed = set(state.get("stages_completed") or [])

    for stage_id, rels, label in GATES:
        paths = [client / r for r in rels]
        if all(p.is_file() for p in paths):
            present.append(stage_id)
            # arithmetic gates
            for p in paths:
                if p.name.startswith("tb_") and p.suffix == ".json":
                    ok, msg = tb_balances(p)
                    if not ok:
                        errors.append(f"{label}: {msg}")
                    else:
                        print(f"  ✓ {label}: {msg}")
                elif p.name.startswith("journals") and p.suffix == ".json":
                    ok, msg = journals_balance(p)
                    if not ok:
                        errors.append(f"{label}: {msg}")
                    else:
                        print(f"  ✓ {label}: {msg}")
                else:
                    print(f"  ✓ {label}: {p.relative_to(client)}")
        else:
            if stage_id in completed:
                errors.append(f"stages_completed has {stage_id} but missing {rels}")
            elif args.require_atb and stage_id == "adjusted_trial_balance":
                errors.append(f"required gate missing: {label}")
            elif args.require_ledger and stage_id == "beancount":
                errors.append(f"required gate missing: {label}")

    # Cross-stage: if ATB present, journals should exist
    if (client / "workpapers/tb_adjusted.json").is_file():
        if not (client / "workpapers/journals.json").is_file():
            warnings.append("ATB present without journals.json")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")

    if errors:
        print(f"FAILED: {len(errors)} gate error(s)")
        return 1
    print(f"OK: stage gates ({len(present)} artifact groups present, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
