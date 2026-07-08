# Industry COA overlays

Industry packs **extend** an entity base COA (`coa_sdn_bhd.json`, etc.). They do not replace entity structure.

## Usage

1. Load base COA for entity type.
2. Merge `overlay_accounts` (overlay wins on same code if intentional rename).
3. Apply `classification_hints` in `classify-transactions`.

## Packs

| File | Industry |
|---|---|
| `trading.json` | Wholesale / retail merchandise |
| `services.json` | Professional / agency services |
| `fnb.json` | Food & beverage |
| `property.json` | Investment property / rental |
| `construction.json` | Contracting / construction |

## Contributing a pack

- Include `industry`, `description`, `base_coa`, `overlay_accounts`, `classification_hints`
- Valid JSON; codes must not collide with unrelated natures without documenting the rename
- No client-specific account names
