"""CLI to run synthetic data generation."""
import argparse
from pathlib import Path
import json

from .generator import generate_all


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic datasets")
    parser.add_argument("--out", "-o", default="data", help="output directory")
    parser.add_argument("--n-customers", type=int, default=100)
    parser.add_argument("--n-orders", type=int, default=500)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    data = generate_all(n_customers=args.n_customers, n_orders=args.n_orders, seed=args.seed)

    customers_path = outdir / "customers.csv"
    orders_path = outdir / "orders.csv"

    data["customers"].to_csv(customers_path, index=False)
    data["orders"].to_csv(orders_path, index=False)

    print(f"Wrote {customers_path} and {orders_path}")


if __name__ == "__main__":
    main()
