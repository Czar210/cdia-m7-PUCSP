# Referencia rapida -- pytest para testes de API

> Use este documento como cola quando estiver escrevendo ou depurando testes.

---

## Comandos essenciais

```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar com traceback resumido
pytest tests/ -v --tb=short

# Parar na primeira falha
pytest tests/ -v -x

# Rodar apenas testes de um arquivo
pytest tests/test_pratos.py -v

# Rodar apenas testes com marcador smoke
pytest tests/ -m smoke -v

# Rodar mostrando prints
pytest tests/ -v -s
```

---

## Estrutura basica de um teste

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_nome_descritivo_do_que_verifica():
    # 1. Preparar (Arrange)
    payload = {"nome": "Margherita", "preco": 45.0}

    # 2. Agir (Act)
    response = client.post("/pratos", json=payload)

    # 3. Verificar (Assert)
    assert response.status_code == 200
    assert response.json()["nome"] == "Margherita"
```

**Padrao Arrange-Act-Assert:** separe mentalmente a preparacao, a acao e a verificacao.

---

## TestClient -- operacoes comuns

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# GET simples
response = client.get("/pratos")

# GET com parametros de query
response = client.get("/pratos?categoria=massa")

# GET por ID
response = client.get("/pratos/1")

# POST com JSON
response = client.post("/pratos", json={"nome": "Pizza", "preco": 40.0})

# PUT
response = client.put("/pratos/1", json={"nome": "Pizza Atualizada"})

# DELETE
response = client.delete("/pratos/1")

# Acessar a resposta
response.status_code        # int (200, 404, 422...)
response.json()             # dict ou list (corpo JSON)
response.text               # string do corpo
response.headers            # headers da resposta
```

---

## Fixtures

### O que e uma fixture

Uma funcao que prepara algo antes do teste e e injetada automaticamente pelo pytest.

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Cria um TestClient para cada teste."""
    return TestClient(app)

# O pytest ve que o parametro se chama 'client'
# e automaticamente executa a fixture antes
def test_raiz(client):
    response = client.get("/")
    assert response.status_code == 200
```

### conftest.py

Arquivo especial que o pytest descobre automaticamente. Fixtures definidas aqui ficam disponiveis para **todos** os arquivos de teste da pasta.

```
tests/
├── conftest.py          <-- fixtures compartilhadas
├── test_pratos.py       <-- usa 'client' sem importar nada
├── test_bebidas.py      <-- usa 'client' sem importar nada
└── test_pedidos.py      <-- usa 'client' sem importar nada
```

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)
```

**Voce NAO precisa importar conftest.py** nos arquivos de teste. O pytest faz isso sozinho.

### Fixture com setup e teardown

```python
@pytest.fixture
def client():
    # Setup (antes do teste)
    app_client = TestClient(app)
    yield app_client
    # Teardown (depois do teste) -- opcional
    # limpar recursos se necessario
```

### Escopos de fixture

```python
@pytest.fixture(scope="function")   # padrao: nova instancia por teste
@pytest.fixture(scope="module")     # uma instancia por arquivo
@pytest.fixture(scope="session")    # uma instancia para todos os testes
```

Para a maioria dos casos, o padrao (`function`) e o mais seguro.

---

## Asserts uteis

```python
# Status code
assert response.status_code == 200
assert response.status_code in [200, 201]

# Tipo da resposta
assert isinstance(response.json(), list)
assert isinstance(response.json(), dict)

# Campo existe
assert "nome" in response.json()
assert "id" in prato

# Valor especifico
assert response.json()["nome"] == "Margherita"

# Lista nao vazia
assert len(response.json()) >= 1

# Tipo do campo
assert isinstance(prato["preco"], (int, float))

# String contem texto
assert "Bella Tavola" in response.json()["mensagem"]

# Todos os itens da lista tem um campo
pratos = response.json()
assert all("nome" in p for p in pratos)

# Valor numerico em faixa
assert 0 < prato["preco"] < 1000
```

---

## Parametrizacao

Testar multiplos casos com uma funcao:

```python
import pytest

@pytest.mark.parametrize("preco_invalido", [-1.0, -0.01, -100.0, 0])
def test_preco_invalido_retorna_422(client, preco_invalido):
    prato = {
        "nome": "Teste",
        "categoria": "massa",
        "preco": preco_invalido,
        "disponivel": True
    }
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422
```

Com multiplos parametros:

```python
@pytest.mark.parametrize("campo,valor_invalido", [
    ("preco", -1.0),
    ("nome", "AB"),             # muito curto
    ("categoria", "esoterico"), # categoria invalida
])
def test_campo_invalido_retorna_422(client, campo, valor_invalido):
    prato = {"nome": "Teste", "categoria": "massa", "preco": 30.0}
    prato[campo] = valor_invalido
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422
```

---

## Marcadores

### Registrar marcadores (pytest.ini)

```ini
[pytest]
markers =
    smoke: testes basicos que verificam se a API esta no ar
    validacao: testes de validacao de entrada
    integracao: testes que dependem de recursos externos (modelo, banco)
```

### Usar marcadores nos testes

```python
import pytest

@pytest.mark.smoke
def test_api_responde(client):
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.validacao
def test_preco_invalido(client):
    ...

@pytest.mark.integracao
def test_modelo_carrega(client):
    ...
```

### Rodar por marcador

```bash
pytest tests/ -m smoke             # apenas smoke
pytest tests/ -m "not integracao"  # tudo exceto integracao
pytest tests/ -m "smoke or validacao"  # smoke OU validacao
```

---

## Testes frageis vs robustos

| Fragil (evitar) | Robusto (preferir) |
|------------------|-------------------|
| `assert len(pratos) == 6` | `assert len(pratos) >= 1` |
| `assert pratos[0]["nome"] == "Margherita"` | `assert "nome" in pratos[0]` |
| `assert prato["id"] == 7` | `assert isinstance(prato["id"], int)` |
| Depende da ordem de execucao | Funciona em qualquer ordem |

**Principio:** teste comportamento, nao estado interno.

---

## Testes de contrato

Verificam que a API respeita o schema prometido:

```python
def test_contrato_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    # Verifica que todos os campos existem e tem o tipo certo
    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["categoria"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)
```

---

## Lendo output do pytest

```
tests/test_pratos.py::test_listar_pratos PASSED        <-- verde
tests/test_pratos.py::test_criar_prato PASSED           <-- verde
tests/test_pratos.py::test_preco_invalido FAILED        <-- assert falhou
tests/test_modelo.py::test_modelo_carrega ERROR          <-- import/setup falhou

========= 2 passed, 1 failed, 1 error =========
```

* **PASSED:** teste executou e todos os asserts passaram
* **FAILED:** teste executou, mas um assert falhou (bug na API ou no teste)
* **ERROR:** teste nem executou (erro de import, fixture quebrada, dependencia faltando)
