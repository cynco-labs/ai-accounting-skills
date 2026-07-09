#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prove an engagement end-to-end — depth-scoped.

Usage:
  python3 scripts/close_engagement.py fixtures/golden-books-only-mini --no-export-ledger
  python3 scripts/close_engagement.py fixtures/golden-mini-sdn-bhd --no-export-ledger
  python3 scripts/close_engagement.py ./clients/acme --classify --bean-check
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from depth_gates import print_scorecard, score_engagement  # noqa: E402


def run(cmd: list[str]) -> int:
    print(f"→ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser(description="Close / prove engagement (depth-scoped)")
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
    ap.add_argument("--depth", help="Override engagement_type for gates")
    ap.add_argument("--coa", type=Path, default=ROOT / "references/coa_templates/coa_sdn_bhd.json")
    args = ap.parse_args()

    client = args.client_dir.resolve()
    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    print("")
    print("══ AI Accounting · close (depth-scoped) ══")
    print(f"client: {client}")
    print("")

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

    # Depth-strict gates (prove)
    code = run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_stage_gates.py"),
            str(client),
            "--strict",
            *(["--depth", args.depth] if args.depth else []),
        ]
    )
    if code != 0:
        print("FAIL: depth stage gates")
        return code

    card = score_engagement(client, strict=True, depth=args.depth)

    export = args.export_ledger and not args.no_export_ledger
    # Books-only: ledger is optional — only export if user wants or journals exist and export flag
    if card.depth == "bookkeeping_only" and not (client / "ledger/main.beancount").is_file():
        # still allow export if requested
        pass

    ledger = client / "ledger/main.beancount"
    if export and (client / "workpapers/journals.json").is_file():
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

    print_scorecard(card)

    print("── Proof card ──")
    state = {}
    sp = client / "engagement_state.json"
    if sp.is_file():
        state = json.loads(sp.read_text(encoding="utf-8"))
        print(f"  entity:     {state.get('legal_name') or state.get('client_slug')}")
        print(f"  depth:      {card.depth_label} ({card.depth})")
        print(f"  framework:  {state.get('framework')}")
        print(f"  stage:      {state.get('current_stage')} / {state.get('status')}")

    # Depth-aware rows only
    rows = [
        ("register", "source/register.md"),
        ("transactions", "workpapers/transactions.json"),
        ("journals", "workpapers/journals.json"),
        ("bank recon", "workpapers/reconciliations"),
        ("TB prelim", "workpapers/tb_preliminary.json"),
    ]
    if card.depth in ("year_end", "year_end_tax"):
        rows.extend(
            [
                ("YE journals", "workpapers/journals_ye.json"),
                ("TB adjusted", "workpapers/tb_adjusted.json"),
                ("statements", "outputs/fs/primary_statements.md"),
                ("notes", "outputs/fs/notes.md"),
                ("QC", "workpapers/qc_report.md"),
            ]
        )
    if card.depth == "year_end_tax":
        rows.append(("tax", "outputs/tax/computation.md"))
    rows.append(("ledger", "ledger/main.beancount"))

    for label, rel in rows:
        p = client / rel
        if p.is_dir():
            mark = "✓" if any(p.glob("bank*.md")) else "·"
            shown = rel if mark == "✓" else "(missing)"
        else:
            mark = "✓" if p.is_file() else "·"
            shown = rel if p.is_file() else "(missing)"
        print(f"  {mark} {label:12} {shown}")

    tb_path = client / "workpapers/tb_adjusted.json"
    if not tb_path.is_file():
        tb_path = client / "workpapers/tb_preliminary.json"
    if tb_path.is_file():
        tb = json.loads(tb_path.read_text(encoding="utf-8"))
        totals = tb.get("totals") or {}
        print(
            f"  TB tie:     DR {totals.get('debit')}  CR {totals.get('credit')}  "
            f"diff {totals.get('difference')} ({tb_path.name})"
        )

    print("")
    print(f"OK: close proof complete for {card.depth_label}")
    print(f"    {card.human_done}")
    print(f"    ledger → {ledger if ledger.is_file() else '(not exported)'}")
    print("    UI     → npx @cynco/accounting-skills fava " + str(client))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
