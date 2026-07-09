#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prove an engagement end-to-end: validate → optional classify → Beancount → summary.

Usage:
  python3 scripts/close_engagement.py fixtures/golden-mini-sdn-bhd
  python3 scripts/close_engagement.py ./clients/acme --classify --bean-check
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f"→ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser(description="Close / prove engagement artifacts")
    ap.add_argument("client_dir", type=Path)
    ap.add_argument("--classify", action="store_true", help="Run deterministic classifier first")
    ap.add_argument(
        "--roll-tb",
        action="store_true",
        help="Re-roll TB from journals before validate (kernel: never freestyle TB)",
    )
    ap.add_argument("--bean-check", action="store_true", default=True)
    ap.add_argument("--no-bean-check", action="store_true")
    ap.add_argument("--export-ledger", action="store_true", default=True)
    ap.add_argument("--no-export-ledger", action="store_true")
    ap.add_argument("--coa", type=Path, default=ROOT / "references/coa_templates/coa_sdn_bhd.json")
    args = ap.parse_args()

    client = args.client_dir.resolve()
    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    print("")
    print("══ AI Accounting · close ══")
    print(f"client: {client}")
    print("")

    # 1) Classify (optional)
    tx_path = client / "workpapers/transactions.json"
    if args.classify and tx_path.is_file():
        code = run(
            [
                sys.executable,
                str(ROOT / "scripts/classify_transactions.py"),
                "--input",
                str(tx_path),
                "--output",
                str(tx_path),
                "--report",
                str(client / "workpapers/classification_review.md"),
            ]
        )
        if code != 0:
            return code

    # 1b) Roll TB from journals (optional re-derive)
    if args.roll_tb and (client / "workpapers/journals.json").is_file():
        code = run(
            [
                sys.executable,
                str(ROOT / "scripts/roll_tb.py"),
                "--client-dir",
                str(client),
                "--both",
            ]
        )
        if code != 0:
            return code

    # 2) Validate workpapers
    code = run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_engagement_artifacts.py"),
            str(client),
        ]
    )
    if code != 0:
        print("FAIL: engagement artifacts invalid — fix before close")
        return code

    # 3) Stage gates
    code = run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_stage_gates.py"),
            str(client),
        ]
    )
    if code != 0:
        print("FAIL: stage gates")
        return code

    # 4) Export Beancount
    export = args.export_ledger and not args.no_export_ledger
    ledger = client / "ledger/main.beancount"
    if export:
        ledger.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable,
            str(ROOT / "scripts/export_to_beancount.py"),
            "--client-dir",
            str(client),
            "--output",
            str(ledger),
        ]
        if args.coa.is_file() and not (client / "workpapers/coa.json").is_file():
            cmd.extend(["--coa", str(args.coa)])
        if args.bean_check and not args.no_bean_check:
            cmd.append("--bean-check")
        code = run(cmd)
        if code != 0:
            return code

    # 5) Summary proof card
    print("")
    print("── Proof card ──")
    state = {}
    sp = client / "engagement_state.json"
    if sp.is_file():
        state = json.loads(sp.read_text(encoding="utf-8"))
        print(f"  entity:     {state.get('legal_name') or state.get('client_slug')}")
        print(f"  framework:  {state.get('framework')}")
        print(f"  stage:      {state.get('current_stage')} / {state.get('status')}")

    for label, rel in [
        ("transactions", "workpapers/transactions.json"),
        ("journals", "workpapers/journals.json"),
        ("TB adjusted", "workpapers/tb_adjusted.json"),
        ("QC", "workpapers/qc_report.md"),
        ("ledger", "ledger/main.beancount"),
    ]:
        p = client / rel
        mark = "✓" if p.is_file() else "·"
        print(f"  {mark} {label:12} {rel if p.is_file() else '(missing)'}")

    if (client / "workpapers/tb_adjusted.json").is_file():
        tb = json.loads((client / "workpapers/tb_adjusted.json").read_text(encoding="utf-8"))
        totals = tb.get("totals") or {}
        print(
            f"  TB tie:     DR {totals.get('debit')}  CR {totals.get('credit')}  "
            f"diff {totals.get('difference')}"
        )

    print("")
    print("OK: close proof complete")
    print(f"    ledger → {ledger if ledger.is_file() else '(not exported)'}")
    print("    UI     → npx @cynco/accounting-skills fava " + str(client))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
