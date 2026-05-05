import pytest


def test_criar_pedido_prato_existente(client):
    pedido = {"prato_id": 1, "quantidade_prato": 2}
    response = client.post("/pedidos/?id_prato=1", json=pedido)
    assert response.status_code == 200
    assert "pedido" in response.json()


def test_criar_pedido_prato_inexistente(client):
    pedido = {"prato_id": 9999, "quantidade_prato": 1}
    response = client.post("/pedidos/?id_prato=9999", json=pedido)
    assert response.status_code == 404


def test_criar_pedido_prato_indisponivel(client):
    # prato 3 (Lasanha Bolonhesa) has disponivel=False
    pedido = {"prato_id": 3, "quantidade_prato": 1}
    response = client.post("/pedidos/?id_prato=3", json=pedido)
    assert response.status_code == 400


def test_criar_pedido_com_bebida(client):
    pedido = {"prato_id": 1, "bebida_id": 1, "quantidade_prato": 1, "quantidade_bebida": 1}
    response = client.post("/pedidos/?id_prato=1&id_bebida=1", json=pedido)
    assert response.status_code == 200


def test_criar_pedido_bebida_inexistente(client):
    pedido = {"prato_id": 1, "bebida_id": 9999, "quantidade_prato": 1, "quantidade_bebida": 1}
    response = client.post("/pedidos/?id_prato=1&id_bebida=9999", json=pedido)
    assert response.status_code == 404
