from faker import Faker
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

fake = Faker()


def generate_customers(n=100, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
    rows = []
    for i in range(n):
        rows.append({
            "customer_id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "created_at": fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        })
    return pd.DataFrame(rows)


def generate_orders(n=200, customers=None, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        Faker.seed(seed)
    rows = []
    customer_ids = list(customers["customer_id"]) if customers is not None else list(range(1, 101))
    menu_items = ["pizza", "burger", "salad", "sushi", "pasta", "sopa"]
    for i in range(n):
        dt = datetime.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
        rows.append({
            "order_id": i + 1,
            "customer_id": random.choice(customer_ids),
            "item": random.choice(menu_items),
            "price": round(random.uniform(5.0, 60.0), 2),
            "created_at": dt.isoformat()
        })
    return pd.DataFrame(rows)


def generate_all(n_customers=100, n_orders=500, seed=None):
    customers = generate_customers(n_customers, seed=seed)
    orders = generate_orders(n_orders, customers=customers, seed=seed)
    return {"customers": customers, "orders": orders}
