import pytest


def test_contrato_get_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(prato.keys())

    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)


def test_contrato_get_bebida(client):
    response = client.get("/bebidas/1")
    assert response.status_code == 200
    bebida = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(bebida.keys())

    assert isinstance(bebida["id"], int)
    assert isinstance(bebida["nome"], str)
    assert isinstance(bebida["preco"], (int, float))


def test_contrato_post_prato(client):
    novo = {
        "nome": "Contrato Teste Prato",
        "categoria": "pizza",
        "preco": 42.0,
        "disponivel": True,
    }
    response = client.post("/pratos/input", json=novo)
    assert response.status_code == 201
    dados = response.json()

    assert "id" in dados
    assert dados["nome"] == novo["nome"]
    assert dados["categoria"] == novo["categoria"]
    assert dados["preco"] == novo["preco"]


def test_contrato_erro_validacao(client):
    response = client.post("/pratos/input", json={"preco": -1})
    assert response.status_code == 422
    erro = response.json()

    assert "erro" in erro
    assert "status" in erro
    assert "detalhes" in erro
    assert erro["status"] == 422
