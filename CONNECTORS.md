# Connectors (MCP)

Skills work with **local files alone**. Connectors make ingestion and filing faster. Nothing here auto-sends filings or client emails without an explicit human action.

## Design rules

1. **Read before write.** Default MCP scopes should be read-only until a skill documents a write path.
2. **Never report a connector as connected** unless a live tool call succeeds. Configured ≠ connected.
3. **Client confidentiality.** Do not sync entire drives into chat; pull only named paths/IDs.
4. **No silent external send.** Email, e-sign, tax portal, or bank payment actions require explicit confirmation.
5. **Fall back gracefully.** If MCP is missing, ask for a file path or paste.

## Recommended connector map

| Connector type | Examples | Used by | Fallback |
|---|---|---|---|
| Document storage | Google Drive, Box, SharePoint, Dropbox | All plugins — source docs, workpapers | User uploads / local paths |
| Messaging | Slack, Teams | QC alerts, query lists, deadline digests | Inline chat only |
| Bank data | Bank CSV export, Open Banking (jurisdiction-specific), spreadsheet sync | `record-transactions`, `bank-reconciliation` | PDF/CSV bank statements |
| Ledger / GL | Xero, QuickBooks, SQL ledger, or other GL APIs | Bookkeeping, TB export | Manual journals / Excel |
| Payroll | Payroll CSV, HRIS export | Payroll classification, statutory payables | Payslips / EA forms |
| E-sign | DocuSign, local PDF sign | Management approval packs | Wet-ink / email confirmation log |
| Tax / registry | LHDN portals, SSM (no unofficial scrapers) | Filing handoff checklists only | Manual filing by human |

## Per-plugin `.mcp.json` (optional)

Plugins may ship a sample `.mcp.json` listing optional servers. Shipping a sample does **not** mean the user is connected. Cold-start `--check-integrations` must probe live.

Example shape:

```json
{
  "mcpServers": {
    "gdrive": {
      "comment": "Optional — authorize in the host client before use"
    }
  }
}
```

## Security

- Prefer OAuth connectors over long-lived API keys in skill text.
- Never commit secrets to this repository.
- Community skills that request new connectors must declare them in trust review (`accounting-builder-hub:skills-qa`).

## Roadmap (non-binding)

| Priority | Connector | Value |
|---|---|---|
| P1 | Drive/SharePoint | Source document pull |
| P1 | Bank CSV normaliser | Faster recon |
| P2 | Xero/QBO read | Opening TB + comparative |
| P2 | Slack digest | Filing deadline watcher |
| P3 | Jurisdiction e-filing assist | Checklist only until certified |

Contributions that add a connector guide under `references/connectors/<name>.md` are welcome.
