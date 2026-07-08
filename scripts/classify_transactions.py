#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Classify bank transactions against COA patterns + optional payee map.

Deterministic first pass — agents only adjudicate low-confidence rows.

Usage:
  python3 scripts/classify_transactions.py \\
    --input workpapers/transactions.json \\
    --output workpapers/transactions.json \\
    --payee-map workpapers/payee_map.json

  python3 scripts/classify_transactions.py --input fixtures/golden-mini-sdn-bhd/workpapers/transactions.json --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATTERNS = ROOT / "references" / "classification_patterns.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def load_payee_map(path: Path | None) -> dict:
    if not path or not path.is_file():
        return {}
    data = load_json(path)
    # accept { "PAYEE": {account_code, account_name} } or list form
    if isinstance(data, list):
        out = {}
        for row in data:
            key = norm(row.get("payee") or row.get("counterparty") or "")
            if key:
                out[key] = row
        return out
    return {norm(k): v for k, v in data.items()}


def match_pattern(desc: str, direction: str | None, patterns: list[dict]) -> dict | None:
    d = norm(desc)
    best = None
    for p in patterns:
        pdir = p.get("direction")
        if pdir and direction and pdir != direction:
            continue
        for token in p.get("match") or []:
            if token.lower() in d:
                conf = float(p.get("confidence") or 0.5)
                if best is None or conf > best["confidence"]:
                    best = {
                        "account_code": p["account_code"],
                        "account_name": p["account_name"],
                        "classification_basis": "pattern",
                        "confidence": conf,
                        "pattern_id": p.get("id"),
                        "matched_token": token,
                    }
                break
    return best


def classify_one(txn: dict, payee_map: dict, patterns: list[dict], suspense: dict, auto_min: float) -> dict:
    out = dict(txn)
    desc = txn.get("description") or ""
    direction = txn.get("direction")
    counterparty = norm(txn.get("counterparty") or "")

    # Preserve human / prior high-confidence classifications unless --force
    existing_conf = txn.get("classification_confidence")
    if txn.get("account_code") and txn.get("classification_basis") in (
        "employee",
        "invoice",
        "prior_year",
    ):
        out.setdefault("classification_confidence", existing_conf if existing_conf is not None else 0.95)
        out.setdefault("needs_review", False)
        return out

    # 1) Payee map (exact normalized counterparty or description contains key)
    hit = None
    if counterparty and counterparty in payee_map:
        hit = payee_map[counterparty]
    else:
        d = norm(desc)
        for key, val in payee_map.items():
            if key and key in d:
                hit = val
                break
    if hit:
        out["account_code"] = hit.get("account_code") or hit.get("code")
        out["account_name"] = hit.get("account_name") or hit.get("name")
        out["classification_basis"] = "prior_year"
        out["classification_confidence"] = float(hit.get("confidence") or 0.95)
        out["needs_review"] = False
        return out

    # 2) Pattern table
    pat = match_pattern(desc, direction, patterns)
    if pat and pat["confidence"] >= auto_min:
        out["account_code"] = pat["account_code"]
        out["account_name"] = pat["account_name"]
        out["classification_basis"] = "pattern"
        out["classification_confidence"] = pat["confidence"]
        out["classification_meta"] = {
            "pattern_id": pat.get("pattern_id"),
            "matched_token": pat.get("matched_token"),
        }
        out["needs_review"] = pat["confidence"] < 0.85
        return out

    if pat:
        # Weak pattern — surface for agent ask, still propose
        out["account_code"] = pat["account_code"]
        out["account_name"] = pat["account_name"]
        out["classification_basis"] = "pattern"
        out["classification_confidence"] = pat["confidence"]
        out["needs_review"] = True
        out["classification_meta"] = {
            "pattern_id": pat.get("pattern_id"),
            "matched_token": pat.get("matched_token"),
            "reason": "below_auto_threshold",
        }
        return out

    # 3) Suspense
    out["account_code"] = suspense.get("account_code", "9999")
    out["account_name"] = suspense.get("account_name", "Suspense")
    out["classification_basis"] = "suspense"
    out["classification_confidence"] = float(suspense.get("confidence") or 0.2)
    out["needs_review"] = True
    return out


def classify_payload(data: dict, payee_map: dict, rules: dict) -> tuple[dict, dict]:
    patterns = rules.get("patterns") or []
    suspense = rules.get("suspense") or {}
    auto_min = float(rules.get("auto_apply_min_confidence") or 0.75)
    txns = [classify_one(t, payee_map, patterns, suspense, auto_min) for t in data.get("transactions") or []]
    out = dict(data)
    out["transactions"] = txns

    stats = {
        "total": len(txns),
        "by_basis": {},
        "needs_review": 0,
        "mean_confidence": 0.0,
    }
    conf_sum = 0.0
    for t in txns:
        b = t.get("classification_basis") or "unknown"
        stats["by_basis"][b] = stats["by_basis"].get(b, 0) + 1
        if t.get("needs_review"):
            stats["needs_review"] += 1
        conf_sum += float(t.get("classification_confidence") or 0)
    stats["mean_confidence"] = round(conf_sum / len(txns), 4) if txns else 0.0
    out["classification_stats"] = stats
    return out, stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Classify transactions (deterministic first pass)")
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--payee-map", type=Path, default=None)
    ap.add_argument("--patterns", type=Path, default=DEFAULT_PATTERNS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", type=Path, default=None, help="Write review queue markdown")
    args = ap.parse_args()

    if not args.input.is_file():
        print(f"ERROR: not found: {args.input}", file=sys.stderr)
        return 1

    data = load_json(args.input)
    rules = load_json(args.patterns) if args.patterns.is_file() else {"patterns": [], "suspense": {}}
    payee_map = load_payee_map(args.payee_map)
    # default payee map beside input
    if not payee_map:
        sibling = args.input.parent / "payee_map.json"
        payee_map = load_payee_map(sibling)

    out, stats = classify_payload(data, payee_map, rules)

    print(
        f"classified {stats['total']} txns · review={stats['needs_review']} · "
        f"mean_conf={stats['mean_confidence']} · basis={stats['by_basis']}"
    )

    if args.report:
        lines = [
            "# Classification review queue",
            "",
            f"- Total: {stats['total']}",
            f"- Needs review: {stats['needs_review']}",
            f"- Mean confidence: {stats['mean_confidence']}",
            "",
            "| Date | Description | Amount | Dir | Code | Name | Conf | Basis |",
            "|---|---|---:|:---:|:---:|---|---:|---|",
        ]
        for t in out["transactions"]:
            if not t.get("needs_review") and not args.dry_run:
                continue
            if not t.get("needs_review") and args.dry_run:
                # dry-run report: only review items unless all
                pass
            if t.get("needs_review"):
                lines.append(
                    f"| {t.get('date','')} | {(t.get('description') or '')[:48]} | "
                    f"{t.get('amount')} | {t.get('direction')} | {t.get('account_code')} | "
                    f"{t.get('account_name')} | {t.get('classification_confidence')} | "
                    f"{t.get('classification_basis')} |"
                )
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote review report {args.report}")

    if args.dry_run:
        return 0

    dest = args.output or args.input
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
