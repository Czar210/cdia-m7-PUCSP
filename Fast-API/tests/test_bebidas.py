import pytest


# --- GET ---

@pytest.mark.smoke
def test_listar_bebidas_retorna_200(client):
    response = client.get("/bebidas")
    assert response.status_code == 200


def test_listar_bebidas_retorna_lista(client):
    data = client.get("/bebidas").json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_buscar_bebida_existente(client):
    response = client.get("/bebidas/1")
    assert response.status_code == 200
    bebida = response.json()
    assert bebida["id"] == 1
    assert "nome" in bebida


def test_buscar_bebida_inexistente(client):
    response = client.get("/bebidas/9999")
    assert response.status_code == 404


def test_filtro_por_categoria(client):
    response = client.get("/bebidas?categoria=vinho")
    assert response.status_code == 200
    bebidas = response.json()
    assert all(b["categoria"] == "vinho" for b in bebidas)


# --- POST ---

def test_criar_bebida_valida(client):
    nova = {
        "nome": "Cerveja Artesanal Teste",
        "categoria": "cerveja",
        "preco": 25.0,
        "volume_ml": 500,
        "disponivel": True,
    }
    response = client.post("/bebidas/input", json=nova)
    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == nova["nome"]
    assert "id" in dados


@pytest.mark.validacao
def test_preco_negativo_retorna_422(client):
    bebida = {
        "nome": "Bebida Teste",
        "categoria": "suco",
        "preco": -5.0,
        "volume_ml": 300,
    }
    response = client.post("/bebidas/input", json=bebida)
    assert response.status_code == 422


@pytest.mark.validacao
def test_categoria_invalida_retorna_422(client):
    bebida = {
        "nome": "Bebida Teste",
        "categoria": "invalida",
        "preco": 10.0,
        "volume_ml": 300,
    }
    response = client.post("/bebidas/input", json=bebida)
    assert response.status_code == 422
