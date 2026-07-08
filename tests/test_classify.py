#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Unit tests — deterministic classification."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from classify_transactions import classify_payload, load_payee_map  # noqa: E402


class ClassifyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = json.loads(
            (ROOT / "references/classification_patterns.json").read_text(encoding="utf-8")
        )
        cls.golden = json.loads(
            (ROOT / "fixtures/golden-mini-sdn-bhd/workpapers/transactions.json").read_text(
                encoding="utf-8"
            )
        )

    def test_golden_patterns(self):
        # strip codes to force re-classify
        data = json.loads(json.dumps(self.golden))
        for t in data["transactions"]:
            t.pop("account_code", None)
            t.pop("account_name", None)
            t.pop("classification_basis", None)
        out, stats = classify_payload(data, {}, self.rules)
        self.assertEqual(stats["total"], 3)
        codes = {t["id"]: t["account_code"] for t in out["transactions"]}
        self.assertEqual(codes["txn-001"], "4000")  # invoice inflow
        self.assertEqual(codes["txn-002"], "5200")  # rent
        self.assertEqual(codes["txn-003"], "5000")  # salary
        self.assertGreaterEqual(stats["mean_confidence"], 0.75)

    def test_payee_map_wins(self):
        data = {
            "transactions": [
                {
                    "id": "t1",
                    "description": "MYSTERY PAYEE XYZ",
                    "amount": 100,
                    "direction": "outflow",
                    "counterparty": "Mystery Payee",
                }
            ]
        }
        payee = {"mystery payee": {"account_code": "5700", "account_name": "Misc", "confidence": 0.99}}
        out, _ = classify_payload(data, payee, self.rules)
        self.assertEqual(out["transactions"][0]["account_code"], "5700")
        self.assertEqual(out["transactions"][0]["classification_basis"], "prior_year")

    def test_suspense_on_unknown(self):
        data = {
            "transactions": [
                {
                    "id": "t1",
                    "description": "ZZZ UNKNOWN COUNTERPARTY 999",
                    "amount": 50,
                    "direction": "outflow",
                }
            ]
        }
        out, stats = classify_payload(data, {}, self.rules)
        self.assertEqual(out["transactions"][0]["classification_basis"], "suspense")
        self.assertTrue(out["transactions"][0]["needs_review"])
        self.assertEqual(stats["needs_review"], 1)


if __name__ == "__main__":
    unittest.main()
