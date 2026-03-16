# Hug — Synthetic Data Generators

Small package with utilities to generate synthetic datasets used in class notebooks.

Usage:

```bash
python -m Hug.generate --out sample_data --n-customers 200 --n-orders 1000 --seed 42
```

API:
- `Hug.generator.generate_customers(n, seed)` -> pandas.DataFrame
- `Hug.generator.generate_orders(n, customers, seed)` -> pandas.DataFrame
- `Hug.generator.generate_all(...)` -> dict of DataFrames
