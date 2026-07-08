#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a client engagement workspace artifacts.

Usage:
  python3 scripts/validate_engagement_artifacts.py path/to/client
  python3 scripts/validate_engagement_artifacts.py fixtures/golden-mini-sdn-bhd --require-stages setup,source_documents

Exits 0 on success, 1 on failure.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "references" / "schemas"
TOL = Decimal("0.005")


def money(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def try_jsonschema(instance, schema_path: Path, label: str, errors: list[str]):
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return  # structural checks still run
    try:
        schema = load_json(schema_path)
        jsonschema.validate(instance=instance, schema=schema)
    except Exception as e:
        errors.append(f"{label}: schema validation failed: {e}")


def check_journals(data: dict, label: str, errors: list[str]):
    for je in data.get("journals") or []:
        je_no = je.get("je_number", "?")
        deb = sum((money(line.get("debit", 0)) for line in je.get("lines") or []), Decimal("0"))
        cre = sum((money(line.get("credit", 0)) for line in je.get("lines") or []), Decimal("0"))
        if abs(deb - cre) > TOL:
            errors.append(f"{label}: {je_no} unbalanced DR={deb} CR={cre}")
        for i, line in enumerate(je.get("lines") or []):
            d, c = money(line.get("debit", 0)), money(line.get("credit", 0))
            if d > 0 and c > 0:
                errors.append(f"{label}: {je_no} line {i} has both debit and credit")
            if d == 0 and c == 0:
                errors.append(f"{label}: {je_no} line {i} is zero on both sides")


def check_tb(data: dict, label: str, errors: list[str]):
    lines = data.get("lines") or []
    deb = sum((money(l.get("debit", 0)) for l in lines), Decimal("0"))
    cre = sum((money(l.get("credit", 0)) for l in lines), Decimal("0"))
    totals = data.get("totals") or {}
    t_deb, t_cre = money(totals.get("debit", deb)), money(totals.get("credit", cre))
    diff = money(totals.get("difference", t_deb - t_cre))
    if abs(deb - t_deb) > TOL or abs(cre - t_cre) > TOL:
        errors.append(f"{label}: totals mismatch lines DR={deb}/{t_deb} CR={cre}/{t_cre}")
    if abs(t_deb - t_cre) > TOL:
        errors.append(f"{label}: TB does not balance DR={t_deb} CR={t_cre}")
    if abs(diff) > TOL:
        errors.append(f"{label}: totals.difference must be 0, got {diff}")
    for l in lines:
        d, c = money(l.get("debit", 0)), money(l.get("credit", 0))
        if d > 0 and c > 0:
            errors.append(f"{label}: account {l.get('account_code')} has both DR and CR")


def check_transactions(data: dict, label: str, errors: list[str]):
    ids = set()
    for t in data.get("transactions") or []:
        tid = t.get("id")
        if tid in ids:
            errors.append(f"{label}: duplicate transaction id {tid}")
        ids.add(tid)
        if money(t.get("amount", 0)) <= 0:
            errors.append(f"{label}: {tid} amount must be > 0")
        if t.get("direction") not in ("inflow", "outflow"):
            errors.append(f"{label}: {tid} invalid direction")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("client_dir", type=Path)
    ap.add_argument(
        "--require-stages",
        default="",
        help="Comma-separated stages that must appear in stages_completed",
    )
    ap.add_argument("--strict-schema", action="store_true", help="Fail if jsonschema missing")
    args = ap.parse_args()
    client = args.client_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    state_path = client / "engagement_state.json"
    if not state_path.is_file():
        errors.append("missing engagement_state.json")
        state = {}
    else:
        state = load_json(state_path)
        try_jsonschema(state, ROOT / "references/engagement_state.schema.json", "engagement_state", errors)
        if args.require_stages:
            need = [s.strip() for s in args.require_stages.split(",") if s.strip()]
            done = set(state.get("stages_completed") or [])
            for s in need:
                if s not in done and state.get("current_stage") != s:
                    # allow current_stage as in-progress without completed
                    if s not in done:
                        warnings.append(f"stage not in stages_completed: {s}")

    artifacts = {
        "transactions": client / "workpapers/transactions.json",
        "journals": client / "workpapers/journals.json",
        "journals_ye": client / "workpapers/journals_ye.json",
        "tb_preliminary": client / "workpapers/tb_preliminary.json",
        "tb_adjusted": client / "workpapers/tb_adjusted.json",
    }

    # schema map
    schema_map = {
        "transactions": SCHEMA_DIR / "transactions.schema.json",
        "journals": SCHEMA_DIR / "journals.schema.json",
        "journals_ye": SCHEMA_DIR / "journals.schema.json",
        "tb_preliminary": SCHEMA_DIR / "trial_balance.schema.json",
        "tb_adjusted": SCHEMA_DIR / "trial_balance.schema.json",
    }

    try:
        import jsonschema  # noqa: F401
        has_js = True
    except ImportError:
        has_js = False
        if args.strict_schema:
            errors.append("jsonschema package not installed (pip install jsonschema)")
        else:
            warnings.append("jsonschema not installed — running arithmetic checks only")

    for key, path in artifacts.items():
        if not path.is_file():
            continue
        data = load_json(path)
        label = str(path.relative_to(client))
        if has_js:
            try_jsonschema(data, schema_map[key], label, errors)
        if key == "transactions":
            check_transactions(data, label, errors)
        elif key in ("journals", "journals_ye"):
            check_journals(data, label, errors)
        elif key.startswith("tb_"):
            check_tb(data, label, errors)

    # If state claims completed stages, require artifacts
    stage_art = {
        "record_transactions": "workpapers/transactions.json",
        "journal_entries": "workpapers/journals.json",
        "preliminary_trial_balance": "workpapers/tb_preliminary.json",
        "year_end_adjustments": "workpapers/journals_ye.json",
        "adjusted_trial_balance": "workpapers/tb_adjusted.json",
        "source_documents": "source/register.md",
        "quality_review": "workpapers/qc_report.md",
    }
    for stage in state.get("stages_completed") or []:
        rel = stage_art.get(stage)
        if rel and not (client / rel).is_file():
            errors.append(f"stages_completed includes {stage} but missing {rel}")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: {client.name} ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
