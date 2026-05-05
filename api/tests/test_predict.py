import os
import pytest

# point to the trained model so tests can run without HF Hub
os.environ.setdefault("MODEL_PATH", str(
    os.path.join(os.path.dirname(__file__), "..", "..", "datagen", "models", "credit_rf.pkl")
))


@pytest.mark.smoke
def test_predict_retorna_200(client):
    payload = {
        "renda_mensal": 5000.0,
        "divida_atual": 500.0,
        "historico_pagamentos": 80,
        "idade": 35,
        "num_dependentes": 1,
    }
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 200


def test_predict_estrutura_resposta(client):
    payload = {
        "renda_mensal": 5000.0,
        "divida_atual": 500.0,
        "historico_pagamentos": 80,
        "idade": 35,
        "num_dependentes": 1,
    }
    data = client.post("/ml/predict", json=payload).json()
    assert "prediction" in data
    assert "probability" in data
    assert "label" in data
    assert "model_version" in data
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["label"] in ["adimplente", "inadimplente"]


@pytest.mark.integracao
def test_predict_alto_risco_vs_baixo_risco(client):
    """High-risk payload should have higher probability than low-risk."""
    alto_risco = {
        "renda_mensal": 1500.0,
        "divida_atual": 3000.0,
        "historico_pagamentos": 20,
        "idade": 22,
        "num_dependentes": 4,
    }
    baixo_risco = {
        "renda_mensal": 10000.0,
        "divida_atual": 100.0,
        "historico_pagamentos": 98,
        "idade": 50,
        "num_dependentes": 0,
    }
    prob_alto = client.post("/ml/predict", json=alto_risco).json()["probability"]
    prob_baixo = client.post("/ml/predict", json=baixo_risco).json()["probability"]
    assert prob_alto > prob_baixo


@pytest.mark.validacao
def test_predict_campo_invalido_retorna_422(client):
    payload = {
        "renda_mensal": -100.0,
        "divida_atual": 500.0,
        "historico_pagamentos": 80,
        "idade": 35,
        "num_dependentes": 1,
    }
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422


@pytest.mark.validacao
def test_predict_campos_faltando_retorna_422(client):
    response = client.post("/ml/predict", json={})
    assert response.status_code == 422


def test_health_retorna_status(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "ok"
    assert data["model"] in ["loaded", "error", "unavailable"]
