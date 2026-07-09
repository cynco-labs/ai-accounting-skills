#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Depth-scoped gates + both golden fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN_YE = ROOT / "fixtures/golden-mini-sdn-bhd"
GOLDEN_BOOKS = ROOT / "fixtures/golden-books-only-mini"
sys.path.insert(0, str(ROOT / "scripts"))

from depth_gates import resolve_depth, score_engagement  # noqa: E402


class DepthGatesTests(unittest.TestCase):
    def test_resolve_depth_aliases(self):
        self.assertEqual(resolve_depth("bookkeeping_only"), "bookkeeping_only")
        self.assertEqual(resolve_depth("compilation"), "year_end")
        self.assertEqual(resolve_depth("unknown"), "bookkeeping_only")
        self.assertEqual(resolve_depth(None), "bookkeeping_only")
        self.assertEqual(resolve_depth("year_end_tax"), "year_end_tax")

    def test_books_only_strict_pass(self):
        card = score_engagement(GOLDEN_BOOKS, strict=True)
        self.assertEqual(card.depth, "bookkeeping_only")
        self.assertTrue(card.passed)
        self.assertTrue(card.required_ok())

    def test_year_end_strict_pass(self):
        card = score_engagement(GOLDEN_YE, strict=True)
        self.assertEqual(card.depth, "year_end")
        self.assertTrue(card.passed)
        self.assertTrue(card.required_ok())

    def test_books_only_does_not_require_atb(self):
        """Missing ATB is fine for bookkeeping_only."""
        self.assertFalse((GOLDEN_BOOKS / "workpapers/tb_adjusted.json").is_file())
        card = score_engagement(GOLDEN_BOOKS, strict=True)
        self.assertTrue(card.required_ok(), card.errors)

    def test_status_done_without_tb_fails(self):
        with tempfile.TemporaryDirectory() as td:
            client = Path(td)
            (client / "source").mkdir()
            (client / "workpapers").mkdir()
            (client / "source/register.md").write_text("# reg\n")
            (client / "engagement_state.json").write_text(
                json.dumps(
                    {
                        "schema_version": "0.0.1",
                        "client_slug": "broken",
                        "legal_name": "Broken",
                        "fy_end": "2025-12-31",
                        "framework": "MPERS",
                        "jurisdiction_pack": "malaysia",
                        "current_stage": "complete",
                        "status": "done",
                        "engagement_type": "bookkeeping_only",
                        "updated_at": "2026-01-01T00:00:00Z",
                    }
                )
            )
            card = score_engagement(client, strict=True)
            self.assertFalse(card.required_ok())
            self.assertTrue(card.errors)

    def test_cli_depth_gates_books(self):
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/depth_gates.py"), str(GOLDEN_BOOKS), "--strict"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Books only", r.stdout)

    def test_close_books_only(self):
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/close_engagement.py"),
                str(GOLDEN_BOOKS),
                "--no-export-ledger",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("bookkeeping_only", r.stdout.lower() + r.stdout)
        self.assertIn("Books only", r.stdout)

    def test_close_year_end(self):
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/close_engagement.py"),
                str(GOLDEN_YE),
                "--no-export-ledger",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Year-end", r.stdout)


if __name__ == "__main__":
    unittest.main()
