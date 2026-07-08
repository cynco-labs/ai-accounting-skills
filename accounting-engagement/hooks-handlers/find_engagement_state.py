#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Locate engagement_state.json near cwd and print a resume banner (plain text)."""
from __future__ import annotations

import json
import os
from pathlib import Path


def find_states(start: Path, max_up: int = 4, max_results: int = 5) -> list[Path]:
    found: list[Path] = []
    cur = start.resolve()
    for _ in range(max_up + 1):
        direct = cur / "engagement_state.json"
        if direct.is_file():
            found.append(direct)
        clients = cur / "clients"
        if clients.is_dir():
            for p in sorted(clients.glob("*/engagement_state.json")):
                found.append(p)
        # fixtures for developers
        fixtures = cur / "fixtures"
        if fixtures.is_dir():
            for p in sorted(fixtures.glob("*/engagement_state.json")):
                found.append(p)
        if cur.parent == cur:
            break
        cur = cur.parent
        if len(found) >= max_results:
            break
    # dedupe
    out: list[Path] = []
    seen = set()
    for p in found:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out[:max_results]


def banner(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return f"- Found {path} but failed to parse: {e}"
    name = data.get("legal_name") or data.get("client_slug") or path.parent.name
    return (
        f"- **{name}** (`{path}`)\n"
        f"  - stage: `{data.get('current_stage')}` | status: `{data.get('status')}`\n"
        f"  - FYE: {data.get('fy_end')} | framework: {data.get('framework')}\n"
        f"  - blockers: {len(data.get('blockers') or [])} | "
        f"open_queries: {len(data.get('open_queries') or [])}\n"
        f"  - resume with skill `resume-engagement` or `full-engagement-pipeline` "
        f"(do not restart from scratch; disk is truth)"
    )


def main() -> int:
    cwd = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    states = find_states(cwd)
    if not states:
        return 0
    lines = [
        "## Accounting engagement detected",
        "",
        "One or more `engagement_state.json` files are nearby. "
        "**Resume from disk** — do not reconstruct numbers from chat memory.",
        "",
    ]
    for p in states:
        lines.append(banner(p))
        lines.append("")
    lines.append(
        "Load `shared/agent-runtime.md` and run artifact validation before advancing stages."
    )
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
