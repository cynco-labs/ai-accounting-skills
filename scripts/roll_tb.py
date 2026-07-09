#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Pure reduce: journal batches → trial balance.

Kernel function (see shared/kernel-contract.md). Agents must not freestyle TB totals.

Usage:
  python3 scripts/roll_tb.py --journals workpapers/journals.json \\
      --kind preliminary --as-of 2025-12-31 --output workpapers/tb_preliminary.json

  python3 scripts/roll_tb.py --client-dir ./clients/acme --both

  python3 scripts/roll_tb.py --client-dir ./fixtures/golden-mini-sdn-bhd --both --check
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


def load_journals(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("journals"), list):
        raise ValueError(f"{path}: missing journals array")
    return data


def assert_je_balanced(je: dict, path: Path) -> None:
    deb = sum((money(ln.get("debit", 0)) for ln in je.get("lines") or []), Decimal("0"))
    cre = sum((money(ln.get("credit", 0)) for ln in je.get("lines") or []), Decimal("0"))
    if abs(deb - cre) > TOL:
        raise ValueError(
            f"{path}: journal {je.get('je_number', '?')} unbalanced DR={deb} CR={cre}"
        )


def roll(journal_paths: list[Path], *, kind: str, as_of: str, client_slug: str, currency: str) -> dict:
    # code -> {debit, credit, name}
    acc: dict[str, dict[str, Any]] = {}

    for path in journal_paths:
        batch = load_journals(path)
        if not client_slug:
            client_slug = str(batch.get("client_slug") or "client")
        if currency == "MYR" and batch.get("currency"):
            currency = str(batch["currency"])
        for je in batch["journals"]:
            assert_je_balanced(je, path)
            for ln in je.get("lines") or []:
                code = str(ln.get("account_code") or "").strip()
                if not code:
                    raise ValueError(f"{path}: blank account_code in {je.get('je_number')}")
                name = str(ln.get("account_name") or code)
                slot = acc.setdefault(
                    code, {"debit": Decimal("0"), "credit": Decimal("0"), "name": name}
                )
                slot["debit"] += money(ln.get("debit", 0))
                slot["credit"] += money(ln.get("credit", 0))
                if name:
                    slot["name"] = name

    lines: list[dict[str, Any]] = []
    for code in sorted(acc.keys()):
        slot = acc[code]
        net = slot["debit"] - slot["credit"]
        if abs(net) <= TOL:
            # zero balance — omit from TB (standard presentation)
            continue
        if net > 0:
            lines.append(
                {
                    "account_code": code,
                    "account_name": slot["name"],
                    "debit": float(net.quantize(MONEY_Q)),
                    "credit": 0.0,
                }
            )
        else:
            lines.append(
                {
                    "account_code": code,
                    "account_name": slot["name"],
                    "debit": 0.0,
                    "credit": float((-net).quantize(MONEY_Q)),
                }
            )

    total_dr = sum((money(l["debit"]) for l in lines), Decimal("0"))
    total_cr = sum((money(l["credit"]) for l in lines), Decimal("0"))
    diff = (total_dr - total_cr).quantize(MONEY_Q)
    if abs(diff) > TOL:
        raise ValueError(f"TB out of balance DR={total_dr} CR={total_cr} diff={diff}")

    return {
        "schema_version": "0.0.1",
        "client_slug": client_slug or "client",
        "as_of": as_of,
        "kind": kind,
        "currency": currency or "MYR",
        "lines": lines,
        "totals": {
            "debit": float(total_dr),
            "credit": float(total_cr),
            "difference": float(diff),
        },
        "source_journals": [str(p) for p in journal_paths],
        "rolled_by": "scripts/roll_tb.py",
    }


def tb_lines_equal(a: dict, b: dict) -> tuple[bool, str]:
    """Compare line sets ignoring order; used by --check."""
    def norm(tb: dict) -> dict[str, tuple[Decimal, Decimal, str]]:
        out = {}
        for ln in tb.get("lines") or []:
            code = str(ln["account_code"])
            out[code] = (money(ln.get("debit", 0)), money(ln.get("credit", 0)), str(ln.get("account_name") or ""))
        return out

    na, nb = norm(a), norm(b)
    if set(na) != set(nb):
        only_a = sorted(set(na) - set(nb))
        only_b = sorted(set(nb) - set(na))
        return False, f"account set differs only_in_rolled={only_a} only_in_expected={only_b}"
    for code in sorted(na):
        if na[code][0] != nb[code][0] or na[code][1] != nb[code][1]:
            return False, f"{code}: rolled DR/CR {na[code][:2]} vs expected {nb[code][:2]}"
    ta = a.get("totals") or {}
    tb = b.get("totals") or {}
    if money(ta.get("debit", 0)) != money(tb.get("debit", 0)):
        return False, f"totals.debit {ta.get('debit')} != {tb.get('debit')}"
    if money(ta.get("credit", 0)) != money(tb.get("credit", 0)):
        return False, f"totals.credit {ta.get('credit')} != {tb.get('credit')}"
    return True, "match"


def resolve_as_of(client: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    state_path = client / "engagement_state.json"
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("fy_end"):
            return str(state["fy_end"])
    return "1970-01-01"


def main() -> int:
    ap = argparse.ArgumentParser(description="Roll journals → trial balance (kernel)")
    ap.add_argument("--journals", type=Path, nargs="*", default=[], help="Journal JSON files")
    ap.add_argument("--kind", choices=["preliminary", "adjusted"], help="TB kind")
    ap.add_argument("--as-of", dest="as_of", default=None)
    ap.add_argument("--client-slug", default="")
    ap.add_argument("--currency", default="MYR")
    ap.add_argument("--output", type=Path, help="Write TB JSON here")
    ap.add_argument("--client-dir", type=Path, help="Engagement root (workpapers/…)")
    ap.add_argument("--preliminary", action="store_true", help="With --client-dir: roll prelim TB")
    ap.add_argument("--adjusted", action="store_true", help="With --client-dir: roll adjusted TB")
    ap.add_argument("--both", action="store_true", help="With --client-dir: prelim + adjusted")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Compare rolled TB to existing file (do not overwrite); exit 1 on mismatch",
    )
    ap.add_argument(
        "--fail-on-empty",
        action="store_true",
        help="Fail if no journal lines produced a TB (empty books)",
    )
    args = ap.parse_args()

    try:
        if args.client_dir:
            client = args.client_dir.resolve()
            wp = client / "workpapers"
            as_of = resolve_as_of(client, args.as_of)
            slug = args.client_slug
            if not slug and (client / "engagement_state.json").is_file():
                slug = json.loads((client / "engagement_state.json").read_text(encoding="utf-8")).get(
                    "client_slug", client.name
                )
            if not slug:
                slug = client.name

            do_prelim = args.both or args.preliminary or (
                not args.adjusted and not args.both and not args.preliminary and not args.kind
            )
            do_adj = args.both or args.adjusted
            if args.kind == "preliminary":
                do_prelim, do_adj = True, False
            elif args.kind == "adjusted":
                do_prelim, do_adj = False, True

            # default with --client-dir alone: both if ye exists else prelim
            if not args.both and not args.preliminary and not args.adjusted and not args.kind:
                do_prelim = True
                do_adj = (wp / "journals_ye.json").is_file()

            jobs: list[tuple[str, list[Path], Path]] = []
            j_main = wp / "journals.json"
            if do_prelim:
                if not j_main.is_file():
                    print(f"ERROR: missing {j_main}", file=sys.stderr)
                    return 1
                jobs.append(("preliminary", [j_main], wp / "tb_preliminary.json"))
            if do_adj:
                paths = [j_main]
                ye = wp / "journals_ye.json"
                if ye.is_file():
                    paths.append(ye)
                elif not j_main.is_file():
                    print(f"ERROR: missing {j_main}", file=sys.stderr)
                    return 1
                jobs.append(("adjusted", paths, wp / "tb_adjusted.json"))

            for kind, paths, out in jobs:
                missing = [p for p in paths if not p.is_file()]
                if missing:
                    print(f"ERROR: missing {missing[0]}", file=sys.stderr)
                    return 1
                tb = roll(paths, kind=kind, as_of=as_of, client_slug=slug, currency=args.currency)
                if args.fail_on_empty and not tb["lines"]:
                    print("ERROR: empty trial balance", file=sys.stderr)
                    return 1
                if args.check:
                    if not out.is_file():
                        print(f"ERROR: --check but missing expected {out}", file=sys.stderr)
                        return 1
                    expected = json.loads(out.read_text(encoding="utf-8"))
                    ok, msg = tb_lines_equal(tb, expected)
                    if not ok:
                        print(f"FAIL: {kind} TB {msg}", file=sys.stderr)
                        return 1
                    print(f"OK: {kind} TB matches {out} (DR={tb['totals']['debit']} CR={tb['totals']['credit']})")
                else:
                    out.parent.mkdir(parents=True, exist_ok=True)
                    # preserve human-authored meta fields we don't own? overwrite cleanly
                    out.write_text(json.dumps(tb, indent=2) + "\n", encoding="utf-8")
                    print(
                        f"OK: wrote {out} kind={kind} "
                        f"DR={tb['totals']['debit']} CR={tb['totals']['credit']} "
                        f"lines={len(tb['lines'])}"
                    )
            return 0

        # Explicit journals mode
        if not args.journals:
            print("ERROR: provide --journals or --client-dir", file=sys.stderr)
            return 1
        if not args.kind:
            print("ERROR: --kind required without --client-dir", file=sys.stderr)
            return 1
        if not args.output and not args.check:
            print("ERROR: --output required", file=sys.stderr)
            return 1
        paths = [p.resolve() for p in args.journals]
        for p in paths:
            if not p.is_file():
                print(f"ERROR: not found: {p}", file=sys.stderr)
                return 1
        as_of = args.as_of or "1970-01-01"
        tb = roll(
            paths,
            kind=args.kind,
            as_of=as_of,
            client_slug=args.client_slug,
            currency=args.currency,
        )
        if args.fail_on_empty and not tb["lines"]:
            print("ERROR: empty trial balance", file=sys.stderr)
            return 1
        out = args.output.resolve() if args.output else None
        if args.check:
            target = out or paths[0].parent / f"tb_{args.kind}.json"
            if not target.is_file():
                print(f"ERROR: --check but missing {target}", file=sys.stderr)
                return 1
            expected = json.loads(target.read_text(encoding="utf-8"))
            ok, msg = tb_lines_equal(tb, expected)
            if not ok:
                print(f"FAIL: {msg}", file=sys.stderr)
                return 1
            print(f"OK: TB matches {target}")
            return 0
        assert out is not None
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(tb, indent=2) + "\n", encoding="utf-8")
        print(
            f"OK: wrote {out} DR={tb['totals']['debit']} CR={tb['totals']['credit']} "
            f"lines={len(tb['lines'])}"
        )
        return 0
    except (ValueError, json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
