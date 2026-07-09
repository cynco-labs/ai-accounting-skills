#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Kernel: post_journals + roll_tb pure functions."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "fixtures/golden-mini-sdn-bhd"


class RollTbTests(unittest.TestCase):
    def test_golden_tb_check(self):
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/roll_tb.py"),
                "--client-dir",
                str(GOLDEN),
                "--both",
                "--check",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("preliminary TB matches", r.stdout)
        self.assertIn("adjusted TB matches", r.stdout)

    def test_unbalanced_journal_fails(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            bad = {
                "schema_version": "0.0.1",
                "client_slug": "x",
                "currency": "MYR",
                "journals": [
                    {
                        "je_number": "JE-001",
                        "date": "2025-01-01",
                        "narration": "bad",
                        "lines": [
                            {
                                "account_code": "1000",
                                "account_name": "Cash",
                                "debit": 100,
                                "credit": 0,
                            },
                            {
                                "account_code": "4000",
                                "account_name": "Rev",
                                "debit": 0,
                                "credit": 50,
                            },
                        ],
                    }
                ],
            }
            jpath = td_path / "journals.json"
            jpath.write_text(json.dumps(bad), encoding="utf-8")
            r = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/roll_tb.py"),
                    "--journals",
                    str(jpath),
                    "--kind",
                    "preliminary",
                    "--as-of",
                    "2025-12-31",
                    "--output",
                    str(td_path / "tb.json"),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("unbalanced", (r.stderr + r.stdout).lower())


class PostJournalsTests(unittest.TestCase):
    def test_post_and_roll_matches_golden_shape(self):
        """Post golden transactions with opening-from-bank → TB ties to golden numbers."""
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            wp = td_path / "workpapers"
            wp.mkdir()
            tx = json.loads((GOLDEN / "workpapers/transactions.json").read_text(encoding="utf-8"))
            (wp / "transactions.json").write_text(json.dumps(tx, indent=2), encoding="utf-8")
            # openings match golden JE-001
            openings = {
                "schema_version": "0.0.1",
                "client_slug": "golden-mini-sdn-bhd",
                "currency": "MYR",
                "journals": json.loads((GOLDEN / "workpapers/journals.json").read_text(encoding="utf-8"))[
                    "journals"
                ][:1],
            }
            (wp / "journals_opening.json").write_text(json.dumps(openings, indent=2), encoding="utf-8")

            r = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/post_journals.py"),
                    "--client-dir",
                    str(td_path),
                    "--bank-code",
                    "1000",
                    "--bank-name",
                    "Cash & Bank",
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

            # YE pack
            ye = json.loads((GOLDEN / "workpapers/journals_ye.json").read_text(encoding="utf-8"))
            (wp / "journals_ye.json").write_text(json.dumps(ye, indent=2), encoding="utf-8")

            r2 = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/roll_tb.py"),
                    "--client-dir",
                    str(td_path),
                    "--both",
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)

            prelim = json.loads((wp / "tb_preliminary.json").read_text(encoding="utf-8"))
            adj = json.loads((wp / "tb_adjusted.json").read_text(encoding="utf-8"))
            self.assertEqual(prelim["totals"]["difference"], 0)
            self.assertEqual(adj["totals"]["difference"], 0)
            self.assertEqual(prelim["totals"]["debit"], 15000.0)
            self.assertEqual(adj["totals"]["debit"], 15800.0)

            # Spot-check cash after YE still 12000
            cash = next(l for l in adj["lines"] if l["account_code"] == "1000")
            self.assertEqual(cash["debit"], 12000.0)


if __name__ == "__main__":
    unittest.main()
