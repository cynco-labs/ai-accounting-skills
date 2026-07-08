#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Integration — golden fixture gates + firm profile resolution."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "fixtures/golden-mini-sdn-bhd"


class CloseAndGatesTests(unittest.TestCase):
    def test_stage_gates_golden(self):
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_stage_gates.py"), str(GOLDEN)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_validate_artifacts_golden(self):
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_engagement_artifacts.py"), str(GOLDEN)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_close_engagement_golden(self):
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/close_engagement.py"),
                str(GOLDEN),
                "--no-export-ledger",  # ledger already present; do not mutate fixture
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Proof card", r.stdout)

    def test_firm_profile_init_and_resolve(self):
        with tempfile.TemporaryDirectory() as td:
            env = {**os.environ, "AI_ACCOUNTING_CONFIG": td}
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts/resolve_firm_profile.py"), "--init", "Test Firm"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            profile = Path(td) / "firm-profile.md"
            self.assertTrue(profile.is_file())
            r2 = subprocess.run(
                [sys.executable, str(ROOT / "scripts/resolve_firm_profile.py"), "--json"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(r2.returncode, 0)
            self.assertIn("Test Firm", profile.read_text(encoding="utf-8") or r2.stdout)


if __name__ == "__main__":
    unittest.main()
