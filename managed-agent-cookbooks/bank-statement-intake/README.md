# Cookbook: Bank statement intake

## Purpose

Watch a drop-folder for new bank statements, inventory them into the client source register, and open a bookkeeping task when a full month arrives.

## Security tier

**Prepare** — may write source-document register updates and draft intake notes; may not post journals without a human-run bookkeeping skill.

## Inputs

- Drop path per client: `clients/<slug>/source/bank/inbox/`
- Supported: PDF, CSV (bank-specific)

## Procedure

1. Detect new files (hash + filename).
2. Classify bank account and period from filename/metadata when possible; else queue for human label.
3. Append to source document register (`/engagement-accounting:source-documents` conventions).
4. If a continuous month set is complete for an account, set readiness flag `bank_month_ready=true` for that period.
5. Do **not** auto-post to GL.

## Outputs

- Updated `source/register.md`
- Optional task note: “Run `/bookkeeping-accounting:record-transactions` for [period]”

## Non-goals

- OCR of poor scans without human QC
- Automatic classification of transactions (that’s the bookkeeping plugin)
