#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Keyword / description routing eval for agent skill discoverability.

Does not call a model — scores each utterance against skill frontmatter
descriptions. Fails if the expected skill is not in the top-K matches.

Usage:
  python3 scripts/eval_utterance_routing.py
  python3 scripts/eval_utterance_routing.py --top-k 3
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "utterance_routing.json"
FM_RE = re.compile(r"^---\n(.*?)\n---", re.S)


def parse_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return ""
    block = m.group(1)
    if "description:" not in block:
        return ""
    after = block.split("description:", 1)[1]
    lines = []
    for line in after.splitlines():
        if lines and re.match(r"^[a-zA-Z0-9_-]+:", line):
            break
        lines.append(line)
    return " ".join(l.strip().lstrip(">").strip() for l in lines if l.strip()).lower()


def tokenize(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", s.lower()))


def load_skills() -> dict[str, str]:
    """skill_name -> description text"""
    out: dict[str, str] = {}
    # Prefer umbrella if present (single install surface)
    umbrella = ROOT / "accounting-engagement" / "skills"
    if umbrella.is_dir():
        for d in umbrella.iterdir():
            sm = d / "SKILL.md"
            if sm.is_file():
                out[d.name] = parse_description(sm)
    # Also index modular plugins (union)
    for sm in ROOT.glob("*/skills/*/SKILL.md"):
        name = sm.parent.name
        if name not in out:
            out[name] = parse_description(sm)
        else:
            # merge tokens from both
            out[name] = out[name] + " " + parse_description(sm)
    return out


def score(utterance: str, description: str) -> float:
    ut = tokenize(utterance)
    dt = tokenize(description)
    if not ut or not dt:
        return 0.0
    overlap = ut & dt
    # weight longer rare-ish tokens slightly by presence only
    return len(overlap) / max(len(ut), 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--evals", type=Path, default=EVALS)
    args = ap.parse_args()

    cases = json.loads(args.evals.read_text(encoding="utf-8"))
    skills = load_skills()
    if not skills:
        print("ERROR: no skills found", file=sys.stderr)
        return 1

    failed = 0
    for i, case in enumerate(cases["cases"], 1):
        utt = case["utterance"]
        expected = case["expected_skill"]
        ranked = sorted(
            ((name, score(utt, desc)) for name, desc in skills.items()),
            key=lambda x: (-x[1], x[0]),
        )
        top = ranked[: args.top_k]
        top_names = [n for n, _ in top]
        acceptable = set(case.get("acceptable_skills") or [])
        acceptable.add(expected)
        # notes may say "X is also" — keep explicit field authoritative
        ok = any(n in acceptable for n in top_names) and (
            expected in top_names or bool(case.get("acceptable_skills"))
        )
        # Prefer: expected in top-k OR any listed acceptable is in top-k when acceptable_skills set
        if case.get("acceptable_skills"):
            ok = bool(set(top_names) & set(case["acceptable_skills"] + [expected]))
        else:
            ok = expected in top_names
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"{status} [{i}] expected={expected} top={top_names}")
        print(f"       utterance: {utt[:100]}")
        if case.get("notes"):
            print(f"       notes: {case['notes']}")

    total = len(cases["cases"])
    print(f"\n{total - failed}/{total} passed (top-{args.top_k})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
