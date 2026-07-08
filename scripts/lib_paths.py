#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Shared path resolution for multi-agent firm config and package root."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Canonical config dir name under XDG / home
CONFIG_DIRNAME = "ai-accounting"
LEGACY_CLAUDE = Path.home() / ".claude/plugins/config/claude-for-accounting"


def firm_profile_candidates() -> list[Path]:
    """Ordered search paths for firm-profile.md (first hit wins)."""
    out: list[Path] = []
    env = os.environ.get("AI_ACCOUNTING_FIRM_PROFILE")
    if env:
        out.append(Path(env).expanduser())
    # Explicit config root override
    cfg = os.environ.get("AI_ACCOUNTING_CONFIG")
    if cfg:
        out.append(Path(cfg).expanduser() / "firm-profile.md")
    # XDG
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        out.append(Path(xdg) / CONFIG_DIRNAME / "firm-profile.md")
    out.append(Path.home() / f".config/{CONFIG_DIRNAME}/firm-profile.md")
    # Project-local
    out.append(Path.cwd() / ".ai-accounting" / "firm-profile.md")
    # Legacy Claude Code plugin path (still supported)
    out.append(LEGACY_CLAUDE / "firm-profile.md")
    return out


def resolve_firm_profile() -> Path | None:
    for p in firm_profile_candidates():
        if p.is_file():
            return p.resolve()
    return None


def firm_config_dir() -> Path:
    """Preferred writable location for new firm profiles (multi-agent)."""
    cfg = os.environ.get("AI_ACCOUNTING_CONFIG")
    if cfg:
        return Path(cfg).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / CONFIG_DIRNAME
    return Path.home() / f".config/{CONFIG_DIRNAME}"
