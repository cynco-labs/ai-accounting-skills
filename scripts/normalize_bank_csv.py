#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Normalize a simple bank CSV into transactions.schema.json shape.

Usage:
  python3 scripts/normalize_bank_csv.py \\
    --input export.csv \\
    --bank-id maybank-001 \\
    --source-file source/bank/export.csv \\
    --client-slug my-client \\
    --output workpapers/transactions_partial.json

Expected columns (case-insensitive, flexible names):
  date, description, amount, direction OR type OR debit/credit, optional balance
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def pick(row: dict, *names: str):
    lower = {k.lower().strip(): v for k, v in row.items()}
    for n in names:
        if n in lower and str(lower[n]).strip() != "":
            return str(lower[n]).strip()
    return None


def parse_amount(s: str) -> float:
    s = s.replace(",", "").replace("RM", "").replace("myr", "").strip()
    s = re.sub(r"[^\d.\-]", "", s)
    return abs(float(s))


def parse_direction(row: dict, amount_raw: str | None) -> str | None:
    d = pick(row, "direction", "type", "dr/cr", "drcr")
    if d:
        dl = d.lower()
        if dl in ("inflow", "credit", "cr", "deposit", "in", "c"):
            return "inflow"
        if dl in ("outflow", "debit", "dr", "withdrawal", "out", "d", "payment"):
            return "outflow"
    debit = pick(row, "debit", "withdrawal", "money out")
    credit = pick(row, "credit", "deposit", "money in")
    if debit and parse_amount(debit) > 0:
        return "outflow"
    if credit and parse_amount(credit) > 0:
        return "inflow"
    if amount_raw and amount_raw.strip().startswith("-"):
        return "outflow"
    return None


def normalize_date(s: str) -> str:
    s = s.strip()
    # DD/MM/YYYY
    m = re.match(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$", s)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    # YYYY-MM-DD
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        return s
    raise ValueError(f"unrecognized date: {s}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--bank-id", required=True)
    ap.add_argument("--source-file", required=True)
    ap.add_argument("--client-slug", default="unknown")
    ap.add_argument("--currency", default="MYR")
    args = ap.parse_args()

    with args.input.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    txns = []
    for i, row in enumerate(rows, 1):
        desc = pick(row, "description", "narration", "details", "particulars")
        date_s = pick(row, "date", "transaction date", "posting date")
        if not desc or not date_s:
            continue
        if desc.upper() in ("OPENING BALANCE", "CLOSING BALANCE"):
            continue
        amount_s = pick(row, "amount", "txn amount", "value")
        debit = pick(row, "debit", "withdrawal")
        credit = pick(row, "credit", "deposit")
        if amount_s:
            amount = parse_amount(amount_s)
        elif debit:
            amount = parse_amount(debit)
        elif credit:
            amount = parse_amount(credit)
        else:
            print(f"WARN: skip row {i}: no amount", file=sys.stderr)
            continue
        direction = parse_direction(row, amount_s)
        if not direction:
            print(f"WARN: skip row {i}: cannot determine direction", file=sys.stderr)
            continue
        bal = pick(row, "balance", "running balance")
        try:
            date = normalize_date(date_s)
        except ValueError as e:
            print(f"WARN: skip row {i}: {e}", file=sys.stderr)
            continue
        txns.append(
            {
                "id": f"txn-{date.replace('-', '')}-{i:04d}",
                "date": date,
                "description": desc,
                "amount": amount,
                "direction": direction,
                "bank_account_id": args.bank_id,
                "running_balance": float(parse_amount(bal)) if bal else None,
                "account_code": None,
                "account_name": None,
                "classification_basis": None,
                "source_file": args.source_file,
                "source_ref": f"row:{i}",
            }
        )

    out = {
        "schema_version": "0.0.1",
        "client_slug": args.client_slug,
        "currency": args.currency,
        "bank_accounts": [{"id": args.bank_id, "name": args.bank_id}],
        "transactions": txns,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"OK: wrote {len(txns)} transactions → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
