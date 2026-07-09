#!/usr/bin/env python3
"""Generate a single-file HTML engagement pack for humans.

Usage:
    python3 scripts/generate_html_report.py clients/<slug>
    python3 scripts/generate_html_report.py clients/<slug> -o outputs/custom.html

Layout contract — LEFT TO RIGHT (not a long top→bottom essay):

  ┌─────────────────────────────────────────────────────────────┐
  │ Header (identity)                              │ DRAFT     │
  ├─────────────────────────────────────────────────────────────┤
  │ Progress: 1 Organize → 2 Extract → … → 6 Prove  (LTR strip)│
  ├──────────────────┬──────────────────┬───────────────────────┤
  │ ACTION CHECKLIST │ AT A GLANCE      │ WHAT WE BOOKED        │
  │ (what you do)    │ + decisions      │ + trial balance       │
  ├──────────────────┴──────────────────┴───────────────────────┤
  │ MATCHES LTR:  Sales gaps  │  Purchase gaps                  │
  └─────────────────────────────────────────────────────────────┘

Black & white, print-friendly. Amounts only from JSON.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def money(v: Any) -> str:
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return "—"


def esc(s: Any) -> str:
    return html.escape("" if s is None else str(s))


def depth_label(depth: str) -> str:
    return {
        "bookkeeping_only": "Books only",
        "compilation": "Compilation",
        "year_end": "Year-end",
        "year_end_tax": "Year-end + tax",
    }.get(depth or "", depth or "Books only")


def status_label(status: str) -> str:
    return {
        "done": "Complete",
        "in_progress": "In progress",
        "waiting_on_user": "Waiting on you",
        "waiting_on_client": "Waiting on client",
        "blocked": "Blocked",
    }.get(status or "", status or "—")


# Fixed B&W design — LTR board, not vertical essay
CSS = """
:root {
  --ink: #111;
  --muted: #555;
  --rule: #bbb;
  --rule-soft: #e0e0e0;
  --bg: #fff;
  --shade: #f5f5f5;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }
body {
  color: var(--ink);
  background: var(--bg);
  font: 13px/1.4 "Helvetica Neue", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}
/* Board fills viewport; primary scroll is rare */
.board {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 16px 18px 20px;
  gap: 12px;
  max-width: 1440px;
  margin: 0 auto;
}
/* ── Header row LTR ── */
.header {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 2px solid var(--ink);
  padding-bottom: 10px;
  flex-shrink: 0;
}
.header h1 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
}
.header .meta { margin: 2px 0 0; color: var(--muted); font-size: 0.88rem; }
.header .right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}
.badge {
  border: 1px solid var(--ink);
  padding: 5px 10px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.draft-note {
  color: var(--muted);
  font-size: 0.78rem;
  max-width: 220px;
  text-align: right;
  line-height: 1.35;
}
/* ── Progress LTR strip ── */
.progress {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  border: 1px solid var(--ink);
  flex-shrink: 0;
  overflow-x: auto;
}
.progress .step {
  flex: 1 1 0;
  min-width: 88px;
  padding: 8px 10px;
  border-right: 1px solid var(--rule);
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}
.progress .step:last-child { border-right: none; }
.progress .num {
  font-weight: 700;
  font-size: 0.75rem;
  width: 1.2rem;
  flex-shrink: 0;
}
.progress .label { font-weight: 600; font-size: 0.88rem; }
.progress .state {
  margin-left: auto;
  font-size: 0.75rem;
  color: var(--muted);
  white-space: nowrap;
}
.progress .step.done .state { color: var(--ink); }
.progress .step.done .state::before { content: "✓ "; }
/* ── Main 3 columns LTR ── */
.main {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  gap: 0;
  flex: 1 1 auto;
  min-height: 0;
  border: 1px solid var(--ink);
}
.col {
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-right: 1px solid var(--ink);
  overflow: auto;
}
.col:last-child { border-right: none; }
.col-actions { flex: 1.15 1 0; }
.col-glance  { flex: 0.95 1 0; background: var(--shade); }
.col-books   { flex: 1.25 1 0; }
.col-head {
  padding: 8px 12px;
  border-bottom: 1px solid var(--ink);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 1;
}
.col-body { padding: 10px 12px 14px; flex: 1; }
/* Action cards — still LTR label|content inside */
.action {
  border: 1px solid var(--ink);
  margin: 0 0 10px;
  background: var(--bg);
}
.action .top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: baseline;
  gap: 8px;
  padding: 8px 10px;
  border-bottom: 1px solid var(--rule-soft);
  background: var(--shade);
}
.action .title { font-weight: 700; font-size: 0.92rem; margin: 0; }
.action .prio {
  font-size: 0.65rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border: 1px solid var(--ink);
  padding: 1px 6px;
  white-space: nowrap;
  flex-shrink: 0;
}
.action .fields { padding: 8px 10px; }
.field {
  display: flex;
  flex-direction: row;
  gap: 10px;
  margin: 0 0 6px;
  font-size: 0.86rem;
}
.field .lab {
  flex: 0 0 88px;
  color: var(--muted);
  font-size: 0.68rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding-top: 2px;
}
.field .val { flex: 1 1 auto; min-width: 0; }
.field ul { margin: 0; padding-left: 1.1rem; }
.field li { margin: 2px 0; }
.empty-ok {
  border: 1px solid var(--ink);
  padding: 12px;
  background: var(--bg);
  font-size: 0.9rem;
}
/* Glance metrics LTR */
.metrics {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  border: 1px solid var(--ink);
  background: var(--bg);
  margin-bottom: 12px;
}
.metric {
  flex: 1 1 46%;
  min-width: 100px;
  padding: 8px 10px;
  border-right: 1px solid var(--rule-soft);
  border-bottom: 1px solid var(--rule-soft);
}
.metric .k {
  display: block;
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--muted);
}
.metric .v {
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  font-size: 1rem;
  margin-top: 2px;
}
.metric .v.ok::before { content: "✓ "; }
.bank-line {
  font-size: 0.8rem;
  color: var(--muted);
  margin: 0 0 12px;
  line-height: 1.35;
}
.decisions { margin: 0; padding: 0; list-style: none; }
.decisions li {
  display: flex;
  flex-direction: row;
  gap: 8px;
  padding: 6px 0;
  border-bottom: 1px solid var(--rule-soft);
  font-size: 0.84rem;
}
.decisions .k {
  flex: 0 0 100px;
  color: var(--muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.decisions .v { flex: 1; font-weight: 500; }
.subhead {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin: 4px 0 8px;
  color: var(--muted);
}
/* Tables compact */
table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--ink);
  font-size: 0.8rem;
  background: var(--bg);
}
th, td {
  padding: 4px 6px;
  border-bottom: 1px solid var(--rule-soft);
  text-align: left;
  vertical-align: top;
}
th {
  background: var(--shade);
  font-size: 0.65rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-weight: 700;
  border-bottom: 1px solid var(--ink);
}
tr:last-child td { border-bottom: none; }
tr.total td {
  border-top: 1px solid var(--ink);
  font-weight: 700;
  background: var(--shade);
}
.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.mono {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.92em;
}
.snap { margin-bottom: 10px; }
.note { color: var(--muted); font-size: 0.78rem; margin: 6px 0 0; }
/* ── Bottom row: matches LTR two panes ── */
.bottom {
  display: flex;
  flex-direction: row;
  gap: 0;
  border: 1px solid var(--ink);
  flex-shrink: 0;
  max-height: 240px;
}
.bottom .pane {
  flex: 1 1 50%;
  min-width: 0;
  overflow: auto;
  border-right: 1px solid var(--ink);
  display: flex;
  flex-direction: column;
}
.bottom .pane:last-child { border-right: none; }
.bottom .pane-head {
  padding: 6px 10px;
  border-bottom: 1px solid var(--ink);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: var(--shade);
  position: sticky;
  top: 0;
}
.bottom .pane-body { padding: 8px 10px; }
footer {
  flex-shrink: 0;
  font-size: 0.75rem;
  color: var(--muted);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
  padding-top: 2px;
}
footer p { margin: 0; }
/* Narrow screens: still LTR where possible, wrap to 1 col only if needed */
@media (max-width: 960px) {
  .main { flex-direction: column; max-height: none; }
  .col { border-right: none; border-bottom: 1px solid var(--ink); max-height: 360px; }
  .col:last-child { border-bottom: none; }
  .bottom { flex-direction: column; max-height: none; }
  .bottom .pane { border-right: none; border-bottom: 1px solid var(--ink); max-height: 220px; }
  .bottom .pane:last-child { border-bottom: none; }
}
@media print {
  .board { max-width: none; min-height: auto; }
  .col, .bottom .pane { overflow: visible; max-height: none; }
  .main, .bottom { break-inside: avoid; }
}
"""


def tb_rows_html(tb: dict | None) -> str:
    rows = (tb or {}).get("rows") or (tb or {}).get("lines") or []
    if not tb or not rows:
        return "<tr><td colspan='4'>No trial balance yet.</td></tr>"
    parts = []
    for r in rows:
        if not (r.get("debit") or r.get("credit")):
            continue
        parts.append(
            "<tr>"
            f"<td class='mono'>{esc(r.get('account') or r.get('account_code'))}</td>"
            f"<td>{esc(r.get('name') or r.get('account_name'))}</td>"
            f"<td class='num'>{money(r.get('debit')) if r.get('debit') else ''}</td>"
            f"<td class='num'>{money(r.get('credit')) if r.get('credit') else ''}</td>"
            "</tr>"
        )
    totals = tb.get("totals") or {}
    parts.append(
        "<tr class='total'>"
        "<td></td><td>Totals</td>"
        f"<td class='num'>{money(totals.get('debit'))}</td>"
        f"<td class='num'>{money(totals.get('credit'))}</td>"
        "</tr>"
    )
    return "\n".join(parts) if parts else "<tr><td colspan='4'>Empty.</td></tr>"


def match_table_body(rows: list[dict], kind: str) -> str:
    if not rows:
        return "<p class='note'>None in this pack.</p>"
    if kind == "sales":
        head = "<th>Invoice</th><th>Customer</th><th class='num'>Invoice</th><th class='num'>Bank</th><th class='num'>Gap</th>"
        body = []
        for s in rows:
            body.append(
                "<tr>"
                f"<td class='mono'>{esc(s.get('id'))}</td>"
                f"<td>{esc(s.get('customer'))}</td>"
                f"<td class='num'>{money(s.get('gross'))}</td>"
                f"<td class='num'>{money(s.get('bank_receipt'))}</td>"
                f"<td class='num'>{money(s.get('variance'))}</td>"
                "</tr>"
            )
        note = "Gap + = invoice &gt; bank · Gap − = bank &gt; invoice"
    else:
        head = "<th>Bill</th><th>Supplier</th><th class='num'>Bill</th><th class='num'>Bank</th><th class='num'>Gap</th>"
        body = []
        for b in rows:
            body.append(
                "<tr>"
                f"<td class='mono'>{esc(b.get('id'))}</td>"
                f"<td>{esc(b.get('supplier'))}</td>"
                f"<td class='num'>{money(b.get('gross'))}</td>"
                f"<td class='num'>{money(b.get('bank_paid'))}</td>"
                f"<td class='num'>{money(b.get('variance'))}</td>"
                "</tr>"
            )
        note = "Gap + = bill &gt; paid · Gap − = paid &gt; bill"
    return (
        f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"
        f"<p class='note'>{note}</p>"
    )


def build_action_items(state: dict, tx: dict | None, answers: dict | None) -> list[dict]:
    items: list[dict] = []
    answers = answers or {}
    open_q = state.get("open_queries") or []
    blockers = state.get("blockers") or []

    opening_open = any(
        (isinstance(b, dict) and b.get("id") == "opening-provisional")
        or "opening" in str(b).lower()
        or "prior" in str(b).lower()
        for b in blockers
    ) or any("prior" in str(q).lower() or "opening" in str(q).lower() for q in open_q)

    if opening_open and not answers.get("opening_balances_confirmed"):
        items.append({
            "id": "opening-tb",
            "title": "Confirm opening balances",
            "priority": "Optional",
            "status": "open",
            "why": "Period started from bank open only. Prior equity not on file — retained earnings is a temporary plug.",
            "booked": "Bank opening posted; balancing amount in retained earnings (provisional).",
            "do": [
                "Send last year’s trial balance or signed accounts.",
                "Or reply: keep provisional openings for this pack.",
                "Edge case: brand-new company with no prior year — say so; we label first period.",
            ],
        })

    incomplete = any(
        (isinstance(b, dict) and b.get("id") == "incomplete-year")
        for b in blockers
    )
    if incomplete and state.get("engagement_type") in (None, "bookkeeping_only"):
        items.append({
            "id": "period-scope",
            "title": "Period on file is partial",
            "priority": "Info",
            "status": "open",
            "why": "Only months in your folder were booked. Enough for this period; full-year accounts need the rest.",
            "booked": "Full books depth for months on disk only.",
            "do": [
                "Do nothing if this period is all you wanted.",
                "To upgrade: add missing bank statements and say continue the year.",
                "Edge case: missing middle month — send that statement; we will not invent it.",
            ],
        })

    sales = (tx or {}).get("sales_invoices") or []
    sales_gaps = [s for s in sales if abs(float(s.get("variance") or 0)) >= 0.01]
    if sales_gaps and not answers.get("sales_variances"):
        n = len(sales_gaps)
        total = sum(float(s.get("variance") or 0) for s in sales_gaps)
        items.append({
            "id": "sales-gaps",
            "title": f"Customer payments ≠ invoices ({n})",
            "priority": "Needs you",
            "status": "open",
            "why": f"Invoice vs bank differs on {n} invoice(s); net gap {money(total)}. Choose before debtors or write-offs.",
            "booked": "Sales at bank amount only (cash) until you choose.",
            "do": [
                "Pick in chat: cash only · still owed · credit note · suspense.",
                "Or send customer statements / credit notes.",
                "Edge case: one receipt covers several invoices — give the split.",
            ],
        })
    elif sales_gaps and answers.get("sales_variances"):
        items.append({
            "id": "sales-gaps",
            "title": "Customer gaps — decision recorded",
            "priority": "Done",
            "status": "done",
            "why": "Invoice vs bank differences kept for records; books follow your choice.",
            "booked": f"Policy: {answers.get('sales_variances')}.",
            "do": ["Optional later: send statements to rebook debtors."],
        })

    bills = (tx or {}).get("purchase_bills") or []
    bill_gaps = [b for b in bills if abs(float(b.get("variance") or 0)) >= 0.01]
    if bill_gaps and not answers.get("purchase_variances"):
        n = len(bill_gaps)
        items.append({
            "id": "bill-gaps",
            "title": f"Supplier bills ≠ bank ({n})",
            "priority": "Needs you",
            "status": "open",
            "why": f"{n} bill(s) differ from the bank payment. Some bill text may look wrong — check the match pane.",
            "booked": "Interim: bank as cash expense until you choose.",
            "do": [
                "Pick: keep bank expense · rebook to bill (AP/prepaid) · suspense · corrected invoices.",
                "If one payment covers several bills, list numbers.",
                "Edge case: description looks swapped — confirm nature (utilities, phone, stationery).",
            ],
        })
    elif bill_gaps and answers.get("purchase_variances"):
        items.append({
            "id": "bill-gaps",
            "title": "Supplier gaps — decision recorded",
            "priority": "Done",
            "status": "done",
            "why": "Books follow your purchase policy; AP/prepayments on trial balance.",
            "booked": f"Policy: {answers.get('purchase_variances')}.",
            "do": ["Optional: send corrected supplier invoices if PDFs were wrong."],
        })

    if answers.get("employer_nic") in (None, "") and any(
        "employer" in str(q).lower() or "nic" in str(q).lower() for q in open_q
    ):
        items.append({
            "id": "employer-nic",
            "title": "Employer NIC missing",
            "priority": "Needs you",
            "status": "open",
            "why": "Employee deductions booked; employer NIC not on the document — not invented.",
            "booked": "Gross salaries + employee PAYE/NIC/pension only.",
            "do": [
                "Send employer NIC for the period, or",
                "Reply leave without employer NIC for this pack.",
                "Edge case: do not reuse a prior HMRC total unless you confirm estimate.",
            ],
        })
    elif answers.get("employer_nic"):
        items.append({
            "id": "employer-nic",
            "title": "Employer NIC — decision recorded",
            "priority": "Done",
            "status": "done",
            "why": "Payroll completeness choice saved.",
            "booked": f"Policy: {answers.get('employer_nic')}.",
            "do": ["Optional: provide figure later for an accrual."],
        })

    covered = ("prior", "opening", "sales", "invoice", "bill", "purchase", "employer", "nic", "period")
    for q in open_q:
        ql = str(q).lower()
        if any(h in ql for h in covered):
            continue
        items.append({
            "id": f"q-{abs(hash(q)) % 10000}",
            "title": str(q)[:72],
            "priority": "Needs you",
            "status": "open",
            "why": "Flagged during bookkeeping.",
            "booked": "See trial balance and match panes.",
            "do": [
                "Reply in chat with the document or decision.",
                "Or ask the agent for options.",
            ],
        })

    return items


def actions_html(items: list[dict]) -> str:
    open_items = [i for i in items if i.get("status") != "done"]
    done_items = [i for i in items if i.get("status") == "done"]
    if not open_items and not done_items:
        return (
            "<div class='empty-ok'><strong>Nothing open for you.</strong> "
            "Review the books columns to the right.</div>"
        )
    parts = []
    if not open_items:
        parts.append(
            "<div class='empty-ok' style='margin-bottom:10px'>"
            "<strong>Nothing required from you now.</strong> "
            "Resolved items below for your records.</div>"
        )
    for i in open_items + done_items:
        prio = i.get("priority") or ("Done" if i.get("status") == "done" else "Needs you")
        do_lis = "".join(f"<li>{esc(d)}</li>" for d in (i.get("do") or []))
        parts.append(
            "<div class='action'>"
            f"<div class='top'><p class='title'>{esc(i.get('title'))}</p>"
            f"<span class='prio'>{esc(prio)}</span></div>"
            "<div class='fields'>"
            f"<div class='field'><span class='lab'>Why</span><span class='val'>{esc(i.get('why'))}</span></div>"
            f"<div class='field'><span class='lab'>Booked</span><span class='val'>{esc(i.get('booked'))}</span></div>"
            f"<div class='field'><span class='lab'>You can</span><span class='val'><ul>{do_lis}</ul></span></div>"
            "</div></div>"
        )
    return "\n".join(parts)


def decisions_html(answers: dict | None) -> str:
    if not answers:
        return "<p class='note'>None yet.</p>"
    labels = {
        "soft_confirm": "Entity & period",
        "sales_variances": "Customer gaps",
        "purchase_variances": "Supplier gaps",
        "employer_nic": "Employer NIC",
        "engagement_type": "Depth",
        "opening_balances_confirmed": "Openings",
    }
    skip = {"entity", "currency", "period", "answered_at", "bank"}
    rows = []
    for k, v in answers.items():
        if k in skip or v is None:
            continue
        lab = labels.get(k, k.replace("_", " "))
        rows.append(f"<li><span class='k'>{esc(lab)}</span><span class='v'>{esc(v)}</span></li>")
    if not rows:
        return "<p class='note'>None yet.</p>"
    return f"<ul class='decisions'>{''.join(rows)}</ul>"


def snapshot_html(tb: dict | None, journals: dict | None, currency: str) -> str:
    if not tb:
        return "<p class='note'>No trial balance yet.</p>"
    rows = {(r.get("account") or r.get("account_code")): r for r in (tb.get("rows") or tb.get("lines") or [])}
    je_n = (journals or {}).get("count")
    if je_n is None and journals and "journals" in journals:
        je_n = len(journals["journals"])

    def bal(code: str) -> float:
        r = rows.get(code) or {}
        return float(r.get("debit") or 0) - float(r.get("credit") or 0)

    bank = bal("1300")
    turnover = -bal("5003")
    creditors = -bal("2001")
    prepay = bal("1210")

    lines = [
        f"<p class='note' style='margin-top:0'>{esc(currency)}"
        + (f" · {esc(je_n)} journals" if je_n is not None else "")
        + "</p>",
        "<table class='snap'><tbody>",
        f"<tr><td>Bank</td><td class='num'>{money(bank)}</td></tr>",
    ]
    if turnover:
        lines.append(f"<tr><td>Turnover (services)</td><td class='num'>{money(turnover)}</td></tr>")
    if creditors:
        lines.append(f"<tr><td>Trade creditors</td><td class='num'>{money(creditors)}</td></tr>")
    if prepay:
        lines.append(f"<tr><td>Prepayments</td><td class='num'>{money(prepay)}</td></tr>")
    lines.append("</tbody></table>")
    return "\n".join(lines)


def build_html(client_dir: Path) -> str:
    state = load_json(client_dir / "engagement_state.json") or {}
    tb = load_json(client_dir / "workpapers" / "tb_preliminary.json")
    if not tb:
        tb = load_json(client_dir / "workpapers" / "tb_adjusted.json")
    tx = load_json(client_dir / "workpapers" / "transactions.json")
    answers = load_json(client_dir / "workpapers" / "user_answers.json")
    journals = load_json(client_dir / "workpapers" / "journals.json")
    action_override = load_json(client_dir / "workpapers" / "action_items.json")

    legal = state.get("legal_name") or client_dir.name
    period = f"{state.get('fy_start', '—')}  →  {state.get('fy_end', '—')}"
    currency = state.get("currency") or (tx or {}).get("currency") or ""
    depth = depth_label(state.get("engagement_type") or "bookkeeping_only")
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    status = status_label(state.get("status") or "")

    bank = (tx or {}).get("bank") or {}
    bank_line = ""
    if bank:
        parts = [bank.get("name") or "Bank"]
        if bank.get("sort_code"):
            parts.append(str(bank["sort_code"]))
        if bank.get("account_number"):
            parts.append(str(bank["account_number"]))
        bank_line = (
            f"{esc(' · '.join(parts))}<br/>"
            f"open {money(bank.get('opening_balance'))} → close {money(bank.get('closing_balance'))}"
        )

    balanced = bool(tb and tb.get("balanced"))
    recon = tb.get("bank_recon_diff") if tb else None
    recon_ok = recon is not None and abs(float(recon)) < 0.005
    totals = (tb or {}).get("totals") or {}

    def metric(k: str, v: str, cls: str = "") -> str:
        return (
            f"<div class='metric'><span class='k'>{esc(k)}</span>"
            f"<div class='v {cls}'>{v}</div></div>"
        )

    metrics = (
        "<div class='metrics'>"
        + metric("Bank recon", "0.00" if recon_ok else money(recon), "ok" if recon_ok else "")
        + metric("Trial balance", "Balances" if balanced else "Check", "ok" if balanced else "")
        + metric("Debit", money(totals.get("debit")))
        + metric("Credit", money(totals.get("credit")))
        + metric("Status", esc(status))
        + metric("Depth", esc(depth))
        + "</div>"
    )

    stages = state.get("stages_completed") or []
    job_map = [
        ("1", "Organize", any(s in stages for s in ("smart_intake", "setup", "source_documents"))),
        ("2", "Extract", "record_transactions" in stages),
        ("3", "Classify", "classify_transactions" in stages),
        ("4", "Post", any(s in stages for s in ("journal_entries", "preliminary_trial_balance"))),
        ("5", "Present", True),
        ("6", "Prove", any(s in stages for s in ("bank_reconciliation", "beancount_sor"))),
    ]
    progress = ["<div class='progress'>"]
    for n, name, ok in job_map:
        cls = "done" if ok else ""
        progress.append(
            f"<div class='step {cls}'><span class='num'>{n}</span>"
            f"<span class='label'>{esc(name)}</span>"
            f"<span class='state'>{'Done' if ok else '—'}</span></div>"
        )
    progress.append("</div>")

    if isinstance(action_override, list) and action_override:
        items = action_override
    elif isinstance(action_override, dict) and action_override.get("items"):
        items = action_override["items"]
    else:
        items = build_action_items(state, tx, answers)

    sales = (tx or {}).get("sales_invoices") or []
    bills = (tx or {}).get("purchase_bills") or []

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(legal)} — books pack</title>
<style>{CSS}</style>
</head>
<body>
<div class="board">

  <header class="header">
    <div>
      <h1>{esc(legal)}</h1>
      <p class="meta">{esc(period)} · {esc(currency)} · {esc(depth)} · {esc(generated)}</p>
    </div>
    <div class="right">
      <p class="draft-note">Management pack from source documents. Not signed statutory accounts. Figures from working files only.</p>
      <div class="badge">Draft</div>
    </div>
  </header>

  {"".join(progress)}

  <div class="main">
    <section class="col col-actions">
      <div class="col-head">Action checklist → what you can do</div>
      <div class="col-body">{actions_html(items)}</div>
    </section>

    <section class="col col-glance">
      <div class="col-head">At a glance</div>
      <div class="col-body">
        {metrics}
        {"<p class='bank-line'>" + bank_line + "</p>" if bank_line else ""}
        <div class="subhead">Decisions made</div>
        {decisions_html(answers)}
      </div>
    </section>

    <section class="col col-books">
      <div class="col-head">What we booked · trial balance</div>
      <div class="col-body">
        <div class="subhead">Snapshot</div>
        {snapshot_html(tb, journals, currency)}
        <div class="subhead">Trial balance</div>
        <table>
          <thead>
            <tr><th>Code</th><th>Account</th><th class="num">Debit</th><th class="num">Credit</th></tr>
          </thead>
          <tbody>
            {tb_rows_html(tb)}
          </tbody>
        </table>
      </div>
    </section>
  </div>

  <div class="bottom">
    <div class="pane">
      <div class="pane-head">Customer invoices vs bank →</div>
      <div class="pane-body">{match_table_body(sales, "sales")}</div>
    </div>
    <div class="pane">
      <div class="pane-head">Supplier bills vs bank →</div>
      <div class="pane-body">{match_table_body(bills, "bills")}</div>
    </div>
  </div>

  <footer>
    <p>Read left → right: actions · proof · books · matches.</p>
    <p>Agent files: workpapers JSON · ledger/main.beancount · outputs Excel if any.</p>
  </footer>

</div>
</body>
</html>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate HTML engagement pack")
    ap.add_argument("client", type=Path, help="Path to clients/<slug>")
    ap.add_argument("-o", "--output", type=Path, default=None)
    args = ap.parse_args(argv)

    client_dir = args.client.resolve()
    if not client_dir.is_dir():
        print(f"Not a client directory: {client_dir}", file=sys.stderr)
        return 1

    slug = client_dir.name
    if args.output is None:
        out_dir = client_dir / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{slug}_pack.html"
    else:
        out = args.output.resolve()
        out.parent.mkdir(parents=True, exist_ok=True)

    out.write_text(build_html(client_dir), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
