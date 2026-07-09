#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Depth-scoped engagement gates — single source of truth for Done when.

See references/depth_gates.json and shared/runtime-brief.md.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = ROOT / "references" / "depth_gates.json"
TOL = Decimal("0.005")


def money(x: Any) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class GateResult:
    gate_id: str
    label: str
    ok: bool
    required: bool
    message: str
    path: str | None = None


@dataclass
class ScoreCard:
    depth: str
    depth_label: str
    human_done: str
    client: Path
    status: str
    engagement_type: str | None
    results: list[GateResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def required_ok(self) -> bool:
        return all(r.ok for r in self.results if r.required)


def load_config() -> dict:
    return json.loads(GATES_PATH.read_text(encoding="utf-8"))


def resolve_depth(engagement_type: str | None, config: dict | None = None) -> str:
    cfg = config or load_config()
    raw = (engagement_type or "").strip() or cfg.get("default_depth", "bookkeeping_only")
    aliases = cfg.get("aliases") or {}
    if raw in aliases:
        raw = aliases[raw]
    if raw not in (cfg.get("depths") or {}):
        return cfg.get("default_depth", "bookkeeping_only")
    return raw


def _merge_depth(cfg: dict, depth_id: str) -> dict:
    depths = cfg["depths"]
    node = dict(depths[depth_id])
    if "extends" in node:
        base = _merge_depth(cfg, node["extends"])
        required = list(base.get("required") or [])
        seen = {g["id"] for g in required}
        for g in node.get("required") or []:
            if g["id"] not in seen:
                required.append(g)
                seen.add(g["id"])
        optional = list(base.get("optional") or [])
        oseen = {g["id"] for g in optional}
        for g in node.get("optional") or []:
            if g["id"] not in oseen:
                optional.append(g)
                oseen.add(g["id"])
        return {
            "label": node.get("label") or base.get("label"),
            "human_done": node.get("human_done") or base.get("human_done"),
            "required": required,
            "optional": optional,
            "not_required": node.get("not_required") or base.get("not_required") or [],
        }
    return node


def check_tb(path: Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = data.get("lines") or []
    deb = sum((money(l.get("debit", 0)) for l in lines), Decimal("0"))
    cre = sum((money(l.get("credit", 0)) for l in lines), Decimal("0"))
    if abs(deb - cre) > TOL:
        return False, f"TB out of balance DR={deb} CR={cre}"
    return True, f"balanced DR={deb} CR={cre}"


def check_journals(path: Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    bad = []
    for je in data.get("journals") or []:
        deb = sum((money(l.get("debit", 0)) for l in je.get("lines") or []), Decimal("0"))
        cre = sum((money(l.get("credit", 0)) for l in je.get("lines") or []), Decimal("0"))
        if abs(deb - cre) > TOL:
            bad.append(str(je.get("je_number", "?")))
    n = len(data.get("journals") or [])
    if bad:
        return False, f"unbalanced journals: {', '.join(bad)}"
    if n == 0:
        return False, "no journals in file"
    return True, f"{n} journals balanced"


def check_transactions(path: Path) -> tuple[bool, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    txns = data.get("transactions") or []
    if not txns:
        return False, "no transactions"
    coded = sum(1 for t in txns if t.get("account_code"))
    return True, f"{len(txns)} lines ({coded} coded)"


def check_bank_recon(path: Path) -> tuple[bool, str]:
    """path is file or directory of recon notes."""
    files: list[Path] = []
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = sorted(path.glob("bank*.md")) + sorted(path.glob("**/bank*.md"))
        # de-dupe
        seen = set()
        uniq = []
        for f in files:
            if f.resolve() not in seen:
                seen.add(f.resolve())
                uniq.append(f)
        files = uniq
    if not files:
        return False, "no bank recon file (expected workpapers/reconciliations/bank*.md)"
    # Prefer PASS / difference 0.00
    text = "\n".join(f.read_text(encoding="utf-8") for f in files)
    if re.search(r"(?i)gate:\s*pass", text):
        return True, f"{len(files)} recon file(s); Gate PASS"
    # Difference **0.00** or 0.00 in a recon table row
    if re.search(r"(?i)difference[^\n|]{0,40}\|\s*\**\s*0\.00", text) or re.search(
        r"(?i)\|\s*\**\s*difference\s*\**\s*\|\s*\**\s*0\.00", text
    ):
        return True, f"{len(files)} recon file(s); difference 0.00"
    if re.search(r"(?i)with limitation|amber|limitation", text):
        return True, f"{len(files)} recon file(s); with limitation noted"
    return False, f"{files[0].name}: need Difference 0.00 or Gate: PASS (or with-limitation note)"


def check_qc_section_a(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    if re.search(r"(?i)section\s*a.*pass|pass.*section\s*a|all pass|section a:\s*pass", text):
        return True, "Section A pass noted"
    if re.search(r"(?i)\bPASS\b", text) and not re.search(r"(?i)\bFAIL\b", text):
        return True, "PASS noted (no FAIL)"
    if re.search(r"(?i)\bFAIL\b", text):
        return False, "QC report contains FAIL"
    return False, "QC report present but Section A pass not clear"


def _eval_gate(client: Path, gate: dict) -> GateResult:
    gid = gate["id"]
    label = gate.get("label") or gid
    paths = [client / p for p in gate.get("paths") or []]
    check = gate.get("check")

    # bank_recon: first path may be dir
    if check == "bank_recon":
        target = paths[0] if paths else client / "workpapers/reconciliations"
        if not target.exists():
            return GateResult(gid, label, False, True, "missing bank recon path", str(paths[0]) if paths else None)
        ok, msg = check_bank_recon(target)
        try:
            relp = str(target.relative_to(client))
        except ValueError:
            relp = str(target)
        return GateResult(gid, label, ok, True, msg, relp)

    existing = [p for p in paths if p.is_file()]
    if not existing:
        rels = ", ".join(gate.get("paths") or [])
        return GateResult(gid, label, False, True, f"missing: {rels}", None)

    p = existing[0]
    rel = str(p.relative_to(client))
    if check == "tb":
        ok, msg = check_tb(p)
        return GateResult(gid, label, ok, True, msg, rel)
    if check == "journals":
        ok, msg = check_journals(p)
        return GateResult(gid, label, ok, True, msg, rel)
    if check == "transactions":
        ok, msg = check_transactions(p)
        return GateResult(gid, label, ok, True, msg, rel)
    if check == "qc_section_a":
        ok, msg = check_qc_section_a(p)
        return GateResult(gid, label, ok, True, msg, rel)
    return GateResult(gid, label, True, True, "present", rel)


def score_engagement(
    client: Path,
    *,
    strict: bool | None = None,
    depth: str | None = None,
) -> ScoreCard:
    """Score client dir against depth gates.

    strict=True  → all required gates must pass (prove / status done)
    strict=False → only fail arithmetic on present required files + overclaim handled elsewhere
    strict=None  → auto: True if status in (done,) else False for missing; always fail bad math
    """
    client = client.resolve()
    cfg = load_config()
    state: dict = {}
    sp = client / "engagement_state.json"
    if sp.is_file():
        state = json.loads(sp.read_text(encoding="utf-8"))

    eng_type = depth or state.get("engagement_type")
    depth_id = resolve_depth(eng_type if isinstance(eng_type, str) else None, cfg)
    spec = _merge_depth(cfg, depth_id)
    status = str(state.get("status") or "in_progress")

    if strict is None:
        strict = status in ("done",)

    card = ScoreCard(
        depth=depth_id,
        depth_label=str(spec.get("label") or depth_id),
        human_done=str(spec.get("human_done") or ""),
        client=client,
        status=status,
        engagement_type=state.get("engagement_type"),
    )

    for gate in spec.get("required") or []:
        r = _eval_gate(client, gate)
        r.required = True
        card.results.append(r)
        if not r.ok:
            if strict or (r.path and "balance" in r.message.lower()) or "unbalanced" in r.message.lower():
                # Always fail math; fail missing only when strict
                if "missing" in r.message.lower() and not strict:
                    card.warnings.append(f"{r.label}: {r.message}")
                else:
                    card.errors.append(f"{r.label}: {r.message}")
            else:
                card.warnings.append(f"{r.label}: {r.message}")

    for gate in spec.get("optional") or []:
        r = _eval_gate(client, gate)
        r.required = False
        if r.ok:
            card.results.append(r)
        else:
            card.results.append(
                GateResult(r.gate_id, r.label, False, False, "optional — not present", None)
            )

    # Overclaim: stages_completed names that imply YE when books-only
    completed = set(state.get("stages_completed") or [])
    if depth_id == "bookkeeping_only":
        ye_stages = {
            "year_end_adjustments",
            "adjusted_trial_balance",
            "standards_review",
            "primary_statements",
            "notes",
            "quality_review",
            "finalisation",
            "tax",
        }
        over = sorted(completed & ye_stages)
        for st in over:
            # only error if artifact actually missing for that claim
            pass  # validate_stage_gates still handles missing claimed stages

    # status done but required incomplete
    if status == "done" and not card.required_ok():
        if not any("status done" in e for e in card.errors):
            card.errors.append(
                f"status is done but {card.depth_label} required gates are incomplete"
            )

    return card


def print_scorecard(card: ScoreCard) -> None:
    print("")
    print(f"── Depth scorecard · {card.depth_label} ({card.depth}) ──")
    print(f"  client:  {card.client}")
    print(f"  status:  {card.status}")
    if card.engagement_type:
        print(f"  type:    {card.engagement_type}")
    print("")
    for r in card.results:
        mark = "✓" if r.ok else ("·" if not r.required else "✗")
        req = "req" if r.required else "opt"
        print(f"  {mark} [{req}] {r.label:20} {r.message}")
    for w in card.warnings:
        print(f"  ! {w}")
    for e in card.errors:
        print(f"  ERROR: {e}")
    print("")
    if card.passed and card.required_ok():
        print(f"OK: {card.human_done}")
    elif card.passed:
        print("OK: no hard errors (some required gates still open — job not done yet)")
    else:
        print(f"FAILED: {len(card.errors)} error(s) for depth={card.depth}")
    print("")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Score engagement against depth gates")
    ap.add_argument("client_dir", type=Path)
    ap.add_argument("--depth", help="Override engagement_type")
    ap.add_argument("--strict", action="store_true", help="Require all depth gates (prove)")
    ap.add_argument("--soft", action="store_true", help="Never require missing optional progress")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    client = args.client_dir
    if not client.is_dir():
        print(f"ERROR: not a directory: {client}", file=sys.stderr)
        return 1

    strict: bool | None
    if args.strict:
        strict = True
    elif args.soft:
        strict = False
    else:
        strict = None

    card = score_engagement(client, strict=strict, depth=args.depth)
    if args.json:
        payload = {
            "depth": card.depth,
            "passed": card.passed and card.required_ok(),
            "status": card.status,
            "errors": card.errors,
            "warnings": card.warnings,
            "results": [
                {
                    "id": r.gate_id,
                    "label": r.label,
                    "ok": r.ok,
                    "required": r.required,
                    "message": r.message,
                }
                for r in card.results
            ],
        }
        print(json.dumps(payload, indent=2))
    else:
        print_scorecard(card)

    if not card.passed:
        return 1
    if strict or card.status == "done":
        return 0 if card.required_ok() else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
