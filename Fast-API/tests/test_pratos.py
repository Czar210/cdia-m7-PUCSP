import pytest


# --- GET ---

@pytest.mark.smoke
def test_listar_pratos_retorna_200(client):
    response = client.get("/pratos")
    assert response.status_code == 200


def test_listar_pratos_retorna_lista(client):
    data = client.get("/pratos").json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_buscar_prato_existente(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    assert prato["id"] == 1
    assert "nome" in prato


def test_buscar_prato_inexistente(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404


def test_filtro_por_categoria(client):
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    pratos = response.json()
    assert all(p["categoria"] == "pizza" for p in pratos)


def test_filtro_por_preco_maximo(client):
    response = client.get("/pratos?preco_maximo=30")
    assert response.status_code == 200
    pratos = response.json()
    assert all(p["preco"] <= 30 for p in pratos)


# --- POST ---

def test_criar_prato_valido(client):
    novo = {
        "nome": "Funghi Trifolati Teste",
        "categoria": "massa",
        "preco": 54.0,
        "disponivel": True,
    }
    response = client.post("/pratos/input", json=novo)
    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == novo["nome"]
    assert dados["preco"] == novo["preco"]
    assert "id" in dados


@pytest.mark.validacao
@pytest.mark.parametrize("preco_invalido", [-1.0, -0.01, 0])
def test_preco_invalido_retorna_422(client, preco_invalido):
    prato = {
        "nome": "Prato Teste",
        "categoria": "pizza",
        "preco": preco_invalido,
    }
    response = client.post("/pratos/input", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_categoria_invalida_retorna_422(client):
    prato = {
        "nome": "Prato Teste",
        "categoria": "inexistente",
        "preco": 40.0,
    }
    response = client.post("/pratos/input", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_nome_curto_retorna_422(client):
    prato = {
        "nome": "AB",
        "categoria": "pizza",
        "preco": 40.0,
    }
    response = client.post("/pratos/input", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_campos_obrigatorios_faltando_retorna_422(client):
    response = client.post("/pratos/input", json={})
    assert response.status_code == 422
