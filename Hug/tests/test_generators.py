import pytest
import pandas as pd
from Hug import generator


class TestGenerateCredit:
    def test_basic_shape(self):
        df, X, y = generator.generate_credit(n_samples=100, seed=42)
        assert len(df) == 100
        assert X.shape == (100, 5)
        assert y.shape == (100,)

    def test_columns(self):
        df, _, _ = generator.generate_credit(n_samples=50, seed=1)
        expected = ["renda_mensal", "divida_atual", "historico_pagamentos",
                     "idade", "num_dependentes", "inadimplente"]
        assert list(df.columns) == expected

    def test_target_values(self):
        _, _, y = generator.generate_credit(n_samples=200, seed=7)
        assert set(y).issubset({0, 1})

    def test_reproducibility(self):
        df1, _, _ = generator.generate_credit(n_samples=50, seed=99)
        df2, _, _ = generator.generate_credit(n_samples=50, seed=99)
        pd.testing.assert_frame_equal(df1, df2)

    def test_proportion(self):
        _, _, y = generator.generate_credit(n_samples=2000, seed=42, proporcao_positivos=0.4)
        actual = y.mean()
        assert 0.25 <= actual <= 0.55

    def test_invalid_proportion(self):
        with pytest.raises(ValueError):
            generator.generate_credit(proporcao_positivos=0.0)


class TestGenerateChurn:
    def test_basic_shape(self):
        df, X, y = generator.generate_churn(n_samples=100, seed=42)
        assert len(df) == 100
        assert X.shape == (100, 5)
        assert y.shape == (100,)

    def test_columns(self):
        df, _, _ = generator.generate_churn(n_samples=50, seed=1)
        expected = ["dias_sem_login", "num_chamados", "valor_mensalidade",
                     "meses_contrato", "nps_score", "churn"]
        assert list(df.columns) == expected

    def test_target_values(self):
        _, _, y = generator.generate_churn(n_samples=200, seed=7)
        assert set(y).issubset({0, 1})


class TestGenerateFraud:
    def test_basic_shape(self):
        df, X, y = generator.generate_fraud(n_samples=100, seed=42)
        assert len(df) == 100
        assert X.shape == (100, 5)
        assert y.shape == (100,)

    def test_columns(self):
        df, _, _ = generator.generate_fraud(n_samples=50, seed=1)
        expected = ["amount", "hour", "num_items", "customer_age",
                     "transaction_history_score", "is_fraud"]
        assert list(df.columns) == expected

    def test_low_fraud_rate(self):
        _, _, y = generator.generate_fraud(n_samples=5000, seed=42, proporcao_positivos=0.02)
        actual = y.mean()
        assert actual < 0.10


class TestGenerateAll:
    def test_returns_dict(self):
        result = generator.generate_all(domain="credit")
        assert isinstance(result, dict)
        assert "credit" in result

    def test_generic_domain(self):
        result = generator.generate_all(domain=None)
        assert "dataset" in result
        df = result["dataset"]
        assert "target" in df.columns
