# Parte 2 -- Testes automatizados com pytest

> **Notebook correspondente:** `notebooks/CDIA_CD2_2026_e04_p02_github_actions.ipynb`
>
> **O que voce constroi nesta parte:** Uma suite de testes real contra a API, integrada ao pipeline.

---

## Bloco 3 -- Escrevendo testes e integrando ao pipeline

### Por que testes e nao curl

Na Parte 1, o pipeline verificava se a API subia usando `curl`. Isso e util mas insuficiente:

* O `curl` testa UMA rota
* Nao valida o conteudo da resposta
* Nao testa entradas invalidas
* Nao detecta regressoes em rotas especificas

O pytest resolve tudo isso: voce escreve verificacoes especificas para cada comportamento esperado.

### Estrutura de pastas para testes

```
bella_tavola/
├── main.py
├── requirements.txt
├── routers/
├── models/
└── tests/
    ├── conftest.py          <-- fixtures compartilhadas (Bloco 4)
    ├── test_saude.py        <-- testes basicos
    ├── test_pratos.py       <-- testes de pratos
    ├── test_bebidas.py      <-- testes de bebidas
    └── test_pedidos.py      <-- testes de pedidos
```

### Como o pytest descobre testes

O pytest segue convencoes automaticas:

* Arquivos que comecam com `test_` ou terminam com `_test.py`
* Funcoes dentro desses arquivos que comecam com `test_`

```python
# pytest VAI executar esta:
def test_listar_pratos_retorna_lista():
    ...

# pytest VAI IGNORAR esta:
def verificar_pratos():
    ...
```

### TestClient -- testando sem subir servidor

O `TestClient` do FastAPI permite testar rotas sem servidor rodando. Mais rapido e controlavel que `curl` com `sleep`.

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_raiz_retorna_200():
    response = client.get("/")
    assert response.status_code == 200
```

**O que o TestClient faz internamente:**
1. Cria uma instancia da aplicacao FastAPI em memoria
2. Simula requisicoes HTTP sem abrir porta de rede
3. Retorna objetos `Response` identicos aos de uma requisicao real

### O requirements.txt no contexto de CI

No CI, o `requirements.txt` e a **unica fonte de verdade**. Se uma biblioteca esta na sua maquina mas nao no arquivo, o pipeline falha.

Dependencias necessarias para este projeto:
```
fastapi
uvicorn
pydantic
pydantic-settings
httpx          # necessario para TestClient
pytest         # framework de testes
```

**Regra de ouro:** se voce fez `import X` em qualquer arquivo, `X` deve estar no `requirements.txt`.

### O comando pytest no pipeline

```yaml
- name: Rodar testes
  run: pytest tests/ -v --tb=short
```

| Flag | Efeito |
|------|--------|
| `-v` | Verbose -- mostra o nome de cada teste |
| `--tb=short` | Traceback resumido quando um teste falha |
| `-x` | Para na primeira falha |
| `-s` | Exibe prints durante a execucao |

### Exercicios do Bloco 3

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **3.1** | Essencial | Criar `tests/test_saude.py` com teste minimo e integrar ao pipeline |
| **3.2** | Essencial | Adicionar teste que falha de proposito e observar o pipeline |
| **3.3** | Essencial | Primeiro teste real com TestClient (GET /pratos) |
| **3.4** | Essencial | Testar POST, validacao de entrada, status codes de erro |
| **3.5** | Desafio | Cobertura completa de bebidas e pedidos |

### Passo a passo do exercicio 3.1

1. **Crie a pasta e o arquivo:**
   ```
   tests/test_saude.py
   ```

2. **Escreva o teste minimo:**
   ```python
   def test_pytest_funcionando():
       """Confirma que o pytest encontrou e executou este teste."""
       assert 1 + 1 == 2
   ```

3. **Rode localmente:**
   ```bash
   pytest tests/ -v
   ```

4. **Atualize o `ci.yml`** -- substitua o step de `curl` por:
   ```yaml
   - name: Rodar testes
     run: pytest tests/ -v --tb=short
   ```

5. **Commit + push** e observe na aba Actions

### Passo a passo do exercicio 3.3

Este e onde voce escreve o primeiro teste real:

```python
# tests/test_pratos.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_pratos_retorna_200():
    response = client.get("/pratos")
    assert response.status_code == 200

def test_listar_pratos_retorna_lista():
    response = client.get("/pratos")
    assert isinstance(response.json(), list)

def test_buscar_prato_por_id():
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    assert "nome" in prato

def test_buscar_prato_inexistente():
    response = client.get("/pratos/9999")
    assert response.status_code == 404
```

**Padrao para testar cada rota:**
1. Faca a requisicao com o client
2. Verifique o status code
3. Verifique a estrutura/conteudo da resposta

### Passo a passo do exercicio 3.4

Testar rotas POST e validacao:

```python
def test_criar_prato_valido():
    novo_prato = {
        "nome": "Funghi Trifolati Teste",
        "categoria": "massa",
        "preco": 54.0,
        "disponivel": True
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code in [200, 201]

def test_criar_prato_sem_nome():
    prato_incompleto = {
        "categoria": "massa",
        "preco": 54.0
    }
    response = client.post("/pratos", json=prato_incompleto)
    assert response.status_code == 422   # Validation Error
```

**Status codes importantes:**
| Codigo | Significado | Quando esperar |
|--------|-------------|----------------|
| 200 | OK | GET bem-sucedido, POST em algumas APIs |
| 201 | Created | POST que cria recurso |
| 404 | Not Found | Busca por ID inexistente |
| 422 | Unprocessable Entity | Dados invalidos (Pydantic rejeita) |

---

## Bloco 4 -- Qualidade dos testes

### O problema dos testes acoplados

No Bloco 3, a lista de pratos em memoria persiste entre testes. Isso cria fragilidade:

```python
def test_A():
    client.post("/pratos", json={"nome": "Margherita", ...})
    # cria 1 prato extra

def test_B():
    response = client.get("/pratos")
    assert len(response.json()) == 6   # FALHA se test_A rodou antes!
```

`test_B` depende de `test_A` nao ter rodado. Isso e um **teste acoplado** -- muda o resultado dependendo da ordem de execucao.

### Fixtures do pytest

Uma fixture e uma funcao que prepara dados/recursos antes de um teste. O pytest injeta automaticamente.

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Cria um TestClient para cada teste."""
    return TestClient(app)

# O pytest ve que test_listar_pratos pede 'client'
# e automaticamente chama a fixture antes
def test_listar_pratos(client):
    response = client.get("/pratos")
    assert response.status_code == 200
```

**O que a fixture de `client` resolve:**
* Elimina a variavel global `client = TestClient(app)`
* Organiza melhor o codigo

**O que ela NAO resolve:**
* Nao reinicializa o estado interno da aplicacao (a lista de pratos em memoria continua entre testes)

### conftest.py -- fixtures compartilhadas

Quando varios arquivos de teste precisam da mesma fixture, use `conftest.py`:

```
tests/
├── conftest.py          <-- fixtures disponiveis para TODOS os arquivos
├── test_pratos.py
├── test_bebidas.py
└── test_pedidos.py
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

**O pytest descobre `conftest.py` automaticamente.** Voce nao precisa importa-lo nos testes.

> Para mais detalhes sobre fixtures, veja [referencia-pytest.md](referencia-pytest.md).

### Testes robustos vs frageis

A estrategia para lidar com estado compartilhado: verificar **comportamentos relativos**, nao contagens absolutas.

| Fragil | Robusto |
|--------|---------|
| `assert len(pratos) == 6` | `assert len(pratos) >= 1` |
| `assert pratos[0]["nome"] == "Margherita"` | `assert "nome" in pratos[0]` |
| `assert prato["id"] == 7` | `assert "id" in prato` |

**Principio:** teste que o comportamento esta correto, nao que o estado interno e exatamente o que voce espera.

### Parametrizacao -- multiplos casos, uma funcao

```python
import pytest

@pytest.mark.parametrize("preco_invalido", [-1.0, -0.01, -100.0])
def test_preco_invalido_retorna_422(client, preco_invalido):
    prato = {
        "nome": "Prato Teste",
        "categoria": "massa",
        "preco": preco_invalido,
        "disponivel": True
    }
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422
```

Isso gera **3 testes separados** no pytest, um para cada valor. Muito melhor que copiar a funcao 3 vezes.

### Marcadores -- organizando testes

```python
import pytest

@pytest.mark.smoke
def test_basico_da_api(client):
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.validacao
def test_preco_invalido(client):
    ...
```

Rodar apenas testes smoke:
```bash
pytest tests/ -m smoke
```

Registre os marcadores no `pytest.ini`:
```ini
[pytest]
markers =
    smoke: testes basicos que verificam se a API esta no ar
    validacao: testes de validacao de entrada
    integracao: testes que dependem de recursos externos
```

**No pipeline, marcadores permitem:**
* Rodar testes smoke em PRs (rapido)
* Rodar testes de integracao apenas em push para main (mais completo)

### Exercicios do Bloco 4

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **4.1** | Essencial | Criar `conftest.py` e mover fixture de client |
| **4.2** | Essencial | Reescrever testes frageis para verificar comportamentos |
| **4.3** | Recomendado | Usar `@pytest.mark.parametrize` |
| **4.4** | Recomendado | Criar marcadores e rodar subconjuntos no pipeline |
| **4.5** | Desafio | Testes de contrato (verificar schema completo da resposta) |

---

## Checklist da Parte 2

Ao final, voce deve conseguir:

* [ ] Criar testes com `TestClient` do FastAPI
* [ ] Testar status codes, estrutura de resposta e validacao de entrada (422)
* [ ] Ler os logs do pytest na aba Actions e identificar qual teste falhou
* [ ] Integrar testes ao pipeline com `pytest tests/ -v`
* [ ] Criar e usar fixtures no `conftest.py`
* [ ] Explicar o que a fixture de client resolve e o que nao resolve
* [ ] Reescrever testes frageis para verificar comportamentos relativos
* [ ] Usar `@pytest.mark.parametrize` para multiplos casos
* [ ] Criar marcadores e filtrar testes no pipeline

---

**Anterior:** [Parte 1 -- Fundamentos de CI e GitHub Actions](parte-1-fundamentos-ci.md)
**Proximo:** [Parte 3 -- Integracao com modelo e debugging](parte-3-integracao-debug.md)
