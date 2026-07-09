#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Post classified transactions → balancing journal batch.

Kernel function (see shared/kernel-contract.md).

Bank lines:
  inflow  → DR bank · CR coded account
  outflow → DR coded account · CR bank

Usage:
  python3 scripts/post_journals.py \\
      --transactions workpapers/transactions.json \\
      --output workpapers/journals.json \\
      --openings workpapers/journals_opening.json \\
      --bank-code 1000

  python3 scripts/post_journals.py --client-dir ./clients/acme --bank-code 1000
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

TOL = Decimal("0.005")
MONEY_Q = Decimal("0.01")


def money(x: Any) -> Decimal:
    return Decimal(str(x if x is not None else 0)).quantize(MONEY_Q, rounding=ROUND_HALF_UP)


def fmoney(x: Decimal) -> float:
    return float(x.quantize(MONEY_Q))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def je_balances(je: dict) -> bool:
    deb = sum((money(ln.get("debit", 0)) for ln in je.get("lines") or []), Decimal("0"))
    cre = sum((money(ln.get("credit", 0)) for ln in je.get("lines") or []), Decimal("0"))
    return abs(deb - cre) <= TOL


def bank_name_from_coa_or_default(bank_code: str, bank_name: str) -> str:
    return bank_name or "Cash & Bank"


def post_transactions(
    tx_data: dict,
    *,
    bank_code: str,
    bank_name: str,
    openings: list[dict] | None,
    allow_unclassified: bool,
    suspense_code: str,
    suspense_name: str,
) -> dict:
    slug = str(tx_data.get("client_slug") or "client")
    currency = str(tx_data.get("currency") or "MYR")
    journals: list[dict] = []

    if openings:
        for je in openings:
            if not je_balances(je):
                raise ValueError(f"opening journal {je.get('je_number')} unbalanced")
            journals.append(je)

    seq = 1
    # continue numbering after openings
    for je in journals:
        num = str(je.get("je_number") or "")
        if num.upper().startswith("JE-"):
            try:
                seq = max(seq, int(num.split("-", 1)[1]) + 1)
            except ValueError:
                pass

    bname = bank_name_from_coa_or_default(bank_code, bank_name)
    txns = tx_data.get("transactions") or []
    if not txns:
        raise ValueError("no transactions to post")

    for tx in txns:
        tid = str(tx.get("id") or f"row-{seq}")
        code = tx.get("account_code")
        name = tx.get("account_name") or code
        if not code:
            if allow_unclassified:
                code = suspense_code
                name = suspense_name
            else:
                raise ValueError(
                    f"transaction {tid} missing account_code — classify first "
                    f"or pass --allow-unclassified"
                )
        direction = tx.get("direction")
        if direction not in ("inflow", "outflow"):
            raise ValueError(f"transaction {tid}: direction must be inflow|outflow")
        amt = money(tx.get("amount"))
        if amt <= 0:
            raise ValueError(f"transaction {tid}: amount must be > 0")

        date = str(tx.get("date") or "")
        desc = str(tx.get("description") or tid)
        je_number = f"JE-{seq:03d}"
        seq += 1

        if direction == "inflow":
            lines = [
                {
                    "account_code": bank_code,
                    "account_name": bname,
                    "debit": fmoney(amt),
                    "credit": 0.0,
                },
                {
                    "account_code": str(code),
                    "account_name": str(name),
                    "debit": 0.0,
                    "credit": fmoney(amt),
                },
            ]
        else:
            lines = [
                {
                    "account_code": str(code),
                    "account_name": str(name),
                    "debit": fmoney(amt),
                    "credit": 0.0,
                },
                {
                    "account_code": bank_code,
                    "account_name": bname,
                    "debit": 0.0,
                    "credit": fmoney(amt),
                },
            ]

        je = {
            "je_number": je_number,
            "date": date,
            "narration": desc[:200],
            "source_ref": tid,
            "lines": lines,
        }
        if not je_balances(je):
            raise ValueError(f"internal error: unbalanced JE for {tid}")
        journals.append(je)

    return {
        "schema_version": "0.0.1",
        "client_slug": slug,
        "currency": currency,
        "journals": journals,
        "posted_by": "scripts/post_journals.py",
        "bank_code": bank_code,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Post classified transactions → journals")
    ap.add_argument("--transactions", type=Path, help="transactions.json")
    ap.add_argument("--output", type=Path, help="journals.json")
    ap.add_argument("--openings", type=Path, help="Optional opening journals JSON (same schema)")
    ap.add_argument("--bank-code", default="1000")
    ap.add_argument("--bank-name", default="Cash & Bank")
    ap.add_argument("--client-dir", type=Path)
    ap.add_argument(
        "--allow-unclassified",
        action="store_true",
        help="Post missing codes to suspense (default: fail)",
    )
    ap.add_argument("--suspense-code", default="2900")
    ap.add_argument("--suspense-name", default="Suspense Account")
    ap.add_argument(
        "--opening-from-bank",
        action="store_true",
        help="Synthesize opening JE from bank_accounts[0].opening_balance vs --opening-equity-code",
    )
    ap.add_argument("--opening-equity-code", default="3000")
    ap.add_argument("--opening-equity-name", default="Share Capital")
    ap.add_argument("--opening-date", default=None, help="Date for synthetic opening JE")
    args = ap.parse_args()

    try:
        if args.client_dir:
            client = args.client_dir.resolve()
            tx_path = args.transactions or (client / "workpapers/transactions.json")
            out_path = args.output or (client / "workpapers/journals.json")
            openings_path = args.openings
            if openings_path is None:
                cand = client / "workpapers/journals_opening.json"
                if cand.is_file():
                    openings_path = cand
        else:
            if not args.transactions or not args.output:
                print("ERROR: --transactions and --output required (or --client-dir)", file=sys.stderr)
                return 1
            tx_path = args.transactions
            out_path = args.output
            openings_path = args.openings

        tx_path = tx_path.resolve()
        out_path = out_path.resolve()
        if not tx_path.is_file():
            print(f"ERROR: not found: {tx_path}", file=sys.stderr)
            return 1

        tx_data = load_json(tx_path)
        openings: list[dict] = []
        if openings_path and openings_path.is_file():
            ob = load_json(openings_path.resolve())
            openings = list(ob.get("journals") or [])

        if args.opening_from_bank and not openings:
            banks = tx_data.get("bank_accounts") or []
            if not banks:
                print("ERROR: --opening-from-bank but no bank_accounts in transactions", file=sys.stderr)
                return 1
            b0 = banks[0]
            opening = money(b0.get("opening_balance", 0))
            if opening > 0:
                odate = args.opening_date or str(
                    b0.get("statement_period_start") or "1970-01-01"
                )
                openings = [
                    {
                        "je_number": "JE-001",
                        "date": odate,
                        "narration": "Opening balances (from bank statement opening)",
                        "source_ref": "bank_opening",
                        "lines": [
                            {
                                "account_code": args.bank_code,
                                "account_name": args.bank_name,
                                "debit": fmoney(opening),
                                "credit": 0.0,
                            },
                            {
                                "account_code": args.opening_equity_code,
                                "account_name": args.opening_equity_name,
                                "debit": 0.0,
                                "credit": fmoney(opening),
                            },
                        ],
                    }
                ]
            elif opening < 0:
                print("ERROR: negative bank opening not auto-posted", file=sys.stderr)
                return 1

        batch = post_transactions(
            tx_data,
            bank_code=args.bank_code,
            bank_name=args.bank_name,
            openings=openings or None,
            allow_unclassified=args.allow_unclassified,
            suspense_code=args.suspense_code,
            suspense_name=args.suspense_name,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(batch, indent=2) + "\n", encoding="utf-8")
        print(
            f"OK: wrote {out_path} journals={len(batch['journals'])} "
            f"bank={args.bank_code}"
        )
        return 0
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
