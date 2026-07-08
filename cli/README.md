# `@cynco/accounting-skills` CLI

Thin Node wrapper around the Python scripts in this repo.

```bash
npx @cynco/accounting-skills demo
npx @cynco/accounting-skills close
```

> **Agent skills (`SKILL.md`)** install via [skills.sh](https://skills.sh/cynco-labs/ai-accounting-skills):
>
> ```bash
> npx skills add cynco-labs/ai-accounting-skills
> ```
>
> This npm package is the **deterministic tool layer** (extract · classify · close · ledger).

## Commands

| Command | What it does |
|---|---|
| `demo` | Open golden Beancount ledger in **Fava** |
| `close [client]` | Validate · stage gates · ledger proof card |
| `init [name]` | Scaffold `clients/<slug>/` workspace |
| `extract <path>` | Bank PDF/CSV → Excel (+ JSON) · auto-detect adapter |
| `classify <json>` | Deterministic classify + review markdown |
| `ledger <client>` | Journals → `ledger/main.beancount` (`--fava` optional) |
| `fava [path]` | Serve Fava on a ledger or client dir |
| `firm [--init name]` | Resolve / scaffold multi-agent firm profile |
| `check [client]` | Validate one engagement, or full `ci_check` |
| `doctor` | Python / openpyxl / pdfplumber / beancount / fava |

## Flags

```text
extract <path> [--out file.xlsx] [--json file.json] [--slug name]
classify <json> [--out file.json] [--map payee_map.json] [--report review.md]
close [client] [--classify] [--fava] [--no-ledger]
ledger <client> [--out file.beancount] [--fava]
fava [path] [--port 5000]
firm [--init "Firm Name"]
```

## Requirements

- Node ≥ 18 (for `npx`)
- Python 3
- `pip install -r requirements.txt`

## Publish (maintainers)

```bash
npm publish --access public --otp=XXXXXX
```

Package: `@cynco/accounting-skills` · bins: `accounting-skills`, `ai-accounting`, `cynco-accounting`  
See [PUBLISH.md](../PUBLISH.md).
