# Engagement data schemas

Machine-checkable intermediate formats for agent-native accounting work.

| Schema | Artifact path (typical) |
|---|---|
| `transactions.schema.json` | `workpapers/transactions.json` |
| `journals.schema.json` | `workpapers/journals.json`, `workpapers/journals_ye.json` |
| `trial_balance.schema.json` | `workpapers/tb_preliminary.json`, `workpapers/tb_adjusted.json` |
| `../engagement_state.schema.json` | `engagement_state.json` |

Validate:

```bash
python3 scripts/validate_engagement_artifacts.py path/to/client
python3 scripts/validate_engagement_artifacts.py fixtures/golden-mini-sdn-bhd
```

Rules enforced beyond JSON Schema:

- Each journal: sum(debit) == sum(credit) (tolerance 0.005)
- TB totals: debit == credit and difference == 0 (tolerance 0.005)
- TB line: not both debit and credit non-zero
- Journal line: not both debit and credit non-zero
