#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Unit tests — bank CSV adapters + detection."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_bank import detect, parse_csv_file, rows_to_schema, sniff_csv_bank  # noqa: E402


class ExtractBankTests(unittest.TestCase):
    def test_cimb_sample_parses(self):
        path = ROOT / "fixtures/bank/cimb_sample.csv"
        rows, meta = parse_csv_file(path, "cimb_csv")
        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(rows[0]["direction"], "inflow")
        # balance chain should prove when balances present
        self.assertTrue(meta.get("line_balance_ok") in (True, None) or meta.get("line_balance_ok") is True)
        # Prefer hard true when we have balances
        if meta.get("line_balance_ok") is not None:
            self.assertTrue(meta["line_balance_ok"], msg=meta.get("errors"))

    def test_cimb_balance_proof_strict(self):
        path = ROOT / "fixtures/bank/cimb_sample.csv"
        rows, meta = parse_csv_file(path, "cimb_csv")
        self.assertTrue(meta["line_balance_ok"], msg=meta.get("errors"))
        self.assertEqual(meta["txn_count"], len(rows))

    def test_detect_cimb_fixture(self):
        reports = detect(ROOT / "fixtures/bank/cimb_sample.csv")
        self.assertEqual(len(reports), 1)
        self.assertIn(reports[0]["adapter"], ("cimb_csv", "generic_csv"))
        self.assertTrue(reports[0]["ok"])

    def test_schema_export(self):
        path = ROOT / "fixtures/bank/cimb_sample.csv"
        rows, meta = parse_csv_file(path, "cimb_csv")
        payload = rows_to_schema(rows, [meta], "cimb-demo")
        self.assertEqual(payload["client_slug"], "cimb-demo")
        self.assertEqual(len(payload["transactions"]), len(rows))
        self.assertEqual(payload["transactions"][0]["id"], "txn-0001")

    def test_golden_maybank_csv(self):
        path = ROOT / "fixtures/golden-mini-sdn-bhd/source/bank/maybank_2025.csv"
        rows, meta = parse_csv_file(path, "generic_csv")
        # opening/closing skipped → 3 txns
        self.assertEqual(len(rows), 3)
        dirs = {r["description"]: r["direction"] for r in rows}
        self.assertEqual(dirs["CLIENT PAYMENT INVOICE INV-001"], "inflow")
        self.assertEqual(dirs["SALARY APRIL"], "outflow")


if __name__ == "__main__":
    unittest.main()
