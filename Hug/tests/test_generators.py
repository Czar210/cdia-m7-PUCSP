import pytest
from Hug import generator


def test_generate_customers_basic():
    df = generator.generate_customers(10, seed=123)
    assert len(df) == 10
    assert "customer_id" in df.columns


def test_generate_orders_basic():
    customers = generator.generate_customers(5, seed=1)
    df = generator.generate_orders(20, customers=customers, seed=1)
    assert len(df) == 20
    assert df["customer_id"].isin(customers["customer_id"]).all()
