# `@cynco/accounting-skills` CLI

Thin Node wrapper around the Python scripts in this repo. Built for **DX** and **agents**.

```bash
npx @cynco/accounting-skills demo
```

> **Agent skills (SKILL.md)** install via [skills.sh](https://skills.sh/cynco-labs/ai-accounting-skills), not this package:
>
> ```bash
> npx skills add cynco-labs/ai-accounting-skills
> ```
>
> This npm package is the **CLI** (extract, ledger, Fava, doctor).

## Commands

| Command | What it does |
|---|---|
| `demo` | Open golden Beancount ledger in **Fava** |
| `init [name]` | Scaffold `clients/<slug>/` workspace |
| `extract <path>` | Maybank-style PDF/CSV folder → Excel (+ JSON) |
| `ledger <client>` | Journals → `ledger/main.beancount` (`--fava` optional) |
| `fava [path]` | Serve Fava on a ledger or client dir |
| `check [client]` | Validate one engagement, or full `ci_check` |
| `doctor` | Python / openpyxl / pdfplumber / beancount / fava |

## Flags

```text
extract <path> [--out file.xlsx] [--json file.json] [--slug name]
ledger <client> [--out file.beancount] [--fava]
fava [path] [--port 5000]
```

## Requirements

- Node ≥ 18 (for `npx`)
- Python 3
- `pip install -r requirements.txt` from repo root (or packages the command suggests)

## Publish (maintainers)

From repo root:

```bash
npm publish --access public --otp=XXXXXX
```

Package name: `@cynco/accounting-skills` · bins: `accounting-skills`, `ai-accounting`, `cynco-accounting`

See [PUBLISH.md](../PUBLISH.md).
