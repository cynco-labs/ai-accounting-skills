#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Structural validation for the claude-for-accounting marketplace.

Usage:
  python3 scripts/validate_marketplace.py
  python3 scripts/validate_marketplace.py --strict

Exits 0 on success, 1 on failure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REQUIRED_SKILL_KEYS = {"name", "description"}
# Patterns that must not appear in shipped skill/docs content (private firm lock-in).
# Keep pattern *sources* encoded so this file does not match its own scan.
FIRM_LEAK_PATTERNS = [
    re.compile("hazli" + "johar", re.I),
    re.compile("@" + "hazlijohar" + r"\.", re.I),
    re.compile("NF" + "1932"),
]
SKIP_LEAK_SCAN = {
    "scripts/validate_marketplace.py",
}


def load_marketplace() -> dict:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    block = m.group(1)
    data: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in block.splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:", line):
            if key is not None:
                data[key] = "\n".join(buf).strip()
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == ">" or rest == "|":
                buf = []
            else:
                buf = [rest] if rest else []
        else:
            buf.append(line.strip())
    if key is not None:
        data[key] = "\n".join(buf).strip()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        market = load_marketplace()
    except Exception as e:
        print(f"ERROR: cannot load marketplace.json: {e}", file=sys.stderr)
        return 1

    if market.get("name") != "claude-for-accounting":
        errors.append(f"marketplace name must be 'claude-for-accounting', got {market.get('name')!r}")

    plugins = market.get("plugins") or []
    if not plugins:
        errors.append("marketplace has no plugins")

    seen_names: set[str] = set()
    for entry in plugins:
        name = entry.get("name")
        source = entry.get("source", "")
        if not name:
            errors.append("plugin entry missing name")
            continue
        if name in seen_names:
            errors.append(f"duplicate plugin name: {name}")
        seen_names.add(name)

        plugin_dir = (ROOT / source.lstrip("./")).resolve()
        if not plugin_dir.is_dir():
            errors.append(f"plugin source missing: {source}")
            continue

        pj = plugin_dir / ".claude-plugin" / "plugin.json"
        if not pj.is_file():
            errors.append(f"{name}: missing .claude-plugin/plugin.json")
        else:
            try:
                meta = json.loads(pj.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"{name}: invalid plugin.json: {e}")
                meta = {}
            if meta.get("name") and meta["name"] != name:
                errors.append(f"{name}: plugin.json name {meta['name']!r} != marketplace name")
            if "version" not in meta:
                warnings.append(f"{name}: plugin.json missing version")

        readme = plugin_dir / "README.md"
        if not readme.is_file():
            warnings.append(f"{name}: missing README.md")

        claude = plugin_dir / "CLAUDE.md"
        if not claude.is_file():
            warnings.append(f"{name}: missing CLAUDE.md template")

        skills_root = plugin_dir / "skills"
        if not skills_root.is_dir():
            # builder hub should have skills; stage plugins must
            if name != "accounting-builder-hub":
                errors.append(f"{name}: missing skills/ directory")
            continue

        skill_dirs = [d for d in skills_root.iterdir() if d.is_dir()]
        if not skill_dirs:
            errors.append(f"{name}: skills/ is empty")

        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"{name}: {skill_dir.name} missing SKILL.md")
                continue
            text = skill_md.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if not fm:
                errors.append(f"{name}/{skill_dir.name}: missing YAML frontmatter")
                continue
            missing = REQUIRED_SKILL_KEYS - set(fm)
            if missing:
                errors.append(f"{name}/{skill_dir.name}: frontmatter missing {sorted(missing)}")
            if fm.get("name") and fm["name"] != skill_dir.name:
                warnings.append(
                    f"{name}/{skill_dir.name}: frontmatter name {fm.get('name')!r} != directory name"
                )
            if len(fm.get("description", "")) < 40:
                warnings.append(f"{name}/{skill_dir.name}: description too short for discovery")
            # body must exist
            body = FRONTMATTER_RE.sub("", text, count=1).strip()
            if len(body) < 80:
                warnings.append(f"{name}/{skill_dir.name}: skill body very short")

    # Shared files
    for rel in [
        "shared/guardrails.md",
        "shared/skill-design-framework.md",
        "shared/skill-craft.md",
        "shared/jurisdiction-extension-guide.md",
        "shared/agent-runtime.md",
        "shared/kernel-contract.md",
        "shared/skill-collapse-map.md",
        "shared/classify-substance.md",
        "CONTEXT.md",
        "references/schemas/analysis_pack.example.md",
        "references/pipeline.md",
        "references/stage_artifacts.md",
        "references/engagement_state.schema.json",
        "LICENSE",
        "README.md",
        "QUICKSTART.md",
        "CONTRIBUTING.md",
    ]:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    # Agent-native: default pipeline skill must advertise throw-work triggers
    pipe = ROOT / "engagement-accounting/skills/full-engagement-pipeline/SKILL.md"
    if pipe.is_file():
        ptxt = pipe.read_text(encoding="utf-8")
        for needle in ("engagement_state", "do the books", "bank", "smart-intake"):
            if needle.lower() not in ptxt.lower():
                warnings.append(f"full-engagement-pipeline missing agent-native cue: {needle}")

    # User-invoked only (builder + thin classify aliases)
    for rel in [
        "accounting-builder-hub/skills/skills-qa/SKILL.md",
        "accounting-builder-hub/skills/jurisdiction-scaffold/SKILL.md",
        "accounting-builder-hub/skills/cold-start-interview/SKILL.md",
        "bookkeeping-accounting/skills/revenue-recognition/SKILL.md",
        "bookkeeping-accounting/skills/capitalise-or-expense/SKILL.md",
    ]:
        path = ROOT / rel
        if path.is_file():
            txt = path.read_text(encoding="utf-8")
            if "disable-model-invocation: true" not in txt:
                warnings.append(f"{rel}: should set disable-model-invocation: true")

    # Classify substance doctrine must stay reachable
    classify = ROOT / "bookkeeping-accounting/skills/classify-transactions/SKILL.md"
    if classify.is_file():
        ctxt = classify.read_text(encoding="utf-8")
        for needle in ("classify-substance", "standards_aware", "analysis"):
            if needle not in ctxt:
                warnings.append(f"classify-transactions missing substance cue: {needle}")

    # Umbrella plugin present
    umbrella = ROOT / "accounting-engagement"
    if not (umbrella / ".claude-plugin/plugin.json").is_file():
        errors.append("missing accounting-engagement umbrella plugin")
    else:
        umb_skills = list((umbrella / "skills").glob("*/SKILL.md"))
        if len(umb_skills) < 20:
            warnings.append(f"umbrella has only {len(umb_skills)} skills — run scripts/sync_umbrella.py")

    # Schemas + golden fixture
    for rel in [
        "references/schemas/transactions.schema.json",
        "references/schemas/journals.schema.json",
        "references/schemas/trial_balance.schema.json",
        "fixtures/golden-mini-sdn-bhd/engagement_state.json",
        "evals/utterance_routing.json",
        "scripts/validate_engagement_artifacts.py",
        "scripts/sync_umbrella.py",
        "scripts/eval_utterance_routing.py",
        "scripts/export_to_beancount.py",
        "scripts/extract_maybank_islamic_pdf.py",
        "scripts/ci_check.sh",
        "requirements.txt",
        "shared/architecture.md",
        "shared/excel_deliverables.md",
        "shared/smart-intake.md",
        "references/beancount_integration.md",
        "references/bank_statement_extraction.md",
    ]:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required agent-native file: {rel}")

    # Firm lock-in scan — skills and stage templates only.
    # Maintainer attribution may appear in README/MAINTAINERS/NOTICE/marketplace.
    for path in ROOT.rglob("SKILL.md"):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel in SKIP_LEAK_SCAN:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in FIRM_LEAK_PATTERNS:
            if pat.search(text):
                errors.append(f"firm lock-in in skill (use white-label profile): {rel}")
                break
    # Also scan CLAUDE.md templates under plugins (should stay placeholder)
    for path in ROOT.glob("*/CLAUDE.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = str(path.relative_to(ROOT))
        for pat in FIRM_LEAK_PATTERNS:
            if pat.search(text):
                errors.append(f"firm lock-in in template: {rel}")
                break

    # Config path consistency
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "cynco-accounting-skills" in text and path.name != "CHANGELOG.md":
            # allow historical mention only in changelog
            if "claude-for-accounting" not in text or "cynco-accounting-skills" in text:
                # if old id remains
                if "plugins/config/cynco-accounting-skills" in text or "cynco-accounting-skills@" in text:
                    errors.append(f"old config marketplace id in {path.relative_to(ROOT)}")

    # COA JSON validity
    for coa in (ROOT / "references" / "coa_templates").rglob("*.json"):
        try:
            data = json.loads(coa.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"invalid JSON {coa.relative_to(ROOT)}: {e}")
            continue
        if "accounts" not in data and "overlay_accounts" not in data:
            warnings.append(f"{coa.relative_to(ROOT)}: no accounts/overlay_accounts key")

    for e in errors:
        print(f"ERROR: {e}")
    for w in warnings:
        print(f"WARN:  {w}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if args.strict and warnings:
        print(f"\nFAILED (strict): {len(warnings)} warning(s)")
        return 1
    print(f"OK: marketplace structure valid ({len(plugins)} plugins, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
