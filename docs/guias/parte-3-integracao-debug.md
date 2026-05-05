# Parte 3 -- Integracao com modelo e debugging

> **Notebook correspondente:** `notebooks/CDIA_CD2_2026_e04_p03_github_actions.ipynb`
>
> **O que voce constroi nesta parte:** Pipeline completo que testa o modelo do HF Hub e que voce sabe depurar.

---

## Bloco 5 -- Integrando o modelo do Hugging Face Hub

### O cenario

Na Parte 2, o pipeline testa a API. Mas o endpoint `/ml/predict` depende de um modelo publicado no Hugging Face Hub -- e esse modelo ainda nao esta sendo testado no CI.

O objetivo deste bloco: **o pipeline baixa o modelo do Hub, carrega, e verifica que as predicoes funcionam.**

### Duas abordagens para o modelo no CI

| Abordagem | Vantagem | Desvantagem |
|-----------|----------|-------------|
| Commitar `model.pkl` no Git | Simples, sem dependencia externa | Arquivo binario no Git cresce o repo |
| Baixar do Hugging Face Hub | Modelo versionado separadamente | Precisa de autenticacao (token) |

**Neste projeto, usamos a segunda abordagem** -- e o Hub com `load_model()`.

### Secrets no GitHub Actions

Um **secret** e uma variavel de ambiente protegida. O GitHub:

* **Nunca exibe o valor nos logs** -- mascara com `***`
* Armazena de forma criptografada
* **Nao disponibiliza para PRs de forks externos** (protecao de seguranca)

#### Como criar um secret

1. Va ao repositorio no GitHub
2. **Settings** > **Secrets and variables** > **Actions**
3. Clique **New repository secret**
4. Nome: `HF_TOKEN`
5. Valor: seu token do Hugging Face (comeca com `hf_...`)

#### Como usar no workflow

```yaml
steps:
  - name: Rodar testes de integracao
    run: pytest tests/ -v -m integracao
    env:
      HF_TOKEN: ${{ secrets.HF_TOKEN }}
```

**Atencao:** o erro mais comum e escrever `${{ secret.HF_TOKEN }}` (sem o **s** em `secrets`). Isso passa uma string vazia silenciosamente.

### Checklist antes de testar o modelo no CI

Antes de escrever qualquer teste de integracao, confirme **localmente**:

```bash
# 1. O model_utils.py existe e e importavel
python -c "from model_utils import load_model; print('OK')"

# 2. O modelo carrega sem erro
export HF_TOKEN=hf_seu_token_aqui
python -c "
from model_utils import load_model
model = load_model('seu-usuario/mlops-bella-tavola-v1')
print(type(model))
"

# 3. O endpoint /ml/predict responde
uvicorn main:app --reload
# Em outro terminal:
curl -X POST http://localhost:8000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"valor_pedido": 120.0, "hora_pedido": 20, "num_itens": 3}'
```

**Se qualquer passo falhar, resolva antes de continuar.** Nao adianta testar no CI algo que nao funciona localmente.

### O contrato do modelo e da API

Dois contratos precisam estar alinhados:

**Contrato do modelo:** quais features espera, em qual ordem, com qual tipo.

**Contrato da API:** quais campos o endpoint recebe, como monta o array de features, o que retorna.

Se esses contratos divergem, o modelo recebe features na ordem errada e **retorna predicoes incorretas sem nenhum erro**. Este e exatamente o tipo de problema que CI com bons testes detecta.

### Cache de dependencias no pipeline

Baixar o modelo a cada execucao gasta tempo. Use cache:

```yaml
- name: Cache do modelo Hugging Face
  uses: actions/cache@v4
  with:
    path: ~/.cache/huggingface
    key: hf-model-${{ hashFiles('requirements.txt') }}
```

**Nota sobre a chave:** ela e invalidada quando `requirements.txt` muda. Para invalidar quando o modelo muda, inclua uma versao manual na chave:

```yaml
key: hf-model-v2-${{ hashFiles('requirements.txt') }}
```

### Exercicios do Bloco 5

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **5.1** | Essencial | Configurar secret `HF_TOKEN` e verificar no pipeline |
| **5.2** | Essencial | Baixar e carregar modelo dentro de um teste |
| **5.3** | Essencial | Testar endpoint `/ml/predict` com TestClient |
| **5.4** | Recomendado | Adicionar cache do Hugging Face ao pipeline |
| **5.5** | Desafio | Testes de sanidade do modelo (comportamento faz sentido?) |

### Passo a passo do exercicio 5.1

1. Crie o secret `HF_TOKEN` no GitHub (instrucoes acima)
2. Adicione ao `ci.yml` um step de verificacao:
   ```yaml
   - name: Verificar autenticacao com Hugging Face
     run: python -c "import os; assert os.environ.get('HF_TOKEN'), 'Token nao encontrado'"
     env:
       HF_TOKEN: ${{ secrets.HF_TOKEN }}
   ```
3. Push e observe nos logs -- o valor do token NAO deve aparecer

### Passo a passo do exercicio 5.2

```python
# tests/test_modelo.py
import pytest
import numpy as np

REPO_ID = "seu-usuario/mlops-bella-tavola-v1"  # ajuste
N_FEATURES = 5                                   # ajuste

@pytest.mark.integracao
def test_modelo_carrega():
    from model_utils import load_model
    model = load_model(REPO_ID)
    assert model is not None

@pytest.mark.integracao
def test_modelo_aceita_input_correto():
    from model_utils import load_model
    model = load_model(REPO_ID)
    entrada = np.zeros((1, N_FEATURES))
    resultado = model.predict(entrada)
    assert resultado is not None
    assert len(resultado) == 1
```

### Passo a passo do exercicio 5.3

```python
# Adicionar ao tests/test_modelo.py
PAYLOAD_VALIDO = {
    "valor_pedido": 120.0,
    "hora_pedido": 20,
    "num_itens": 3,
    # ... ajuste para as features do seu modelo
}

@pytest.mark.integracao
def test_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200

@pytest.mark.integracao
def test_predict_retorna_predicao(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    data = response.json()
    assert "prediction" in data or "predicao" in data

@pytest.mark.integracao
def test_predict_payload_invalido(client):
    response = client.post("/ml/predict", json={})
    assert response.status_code == 422
```

### Testes de sanidade do modelo (exercicio 5.5)

Testes de comportamento verificam se o modelo faz sentido:

```python
@pytest.mark.integracao
def test_modelo_distingue_casos_extremos(client):
    """Verifica que o modelo da resultados diferentes para inputs muito diferentes."""
    caso_pequeno = {"valor_pedido": 10.0, "hora_pedido": 10, "num_itens": 1}
    caso_grande = {"valor_pedido": 500.0, "hora_pedido": 22, "num_itens": 10}

    resp_pequeno = client.post("/ml/predict", json=caso_pequeno)
    resp_grande = client.post("/ml/predict", json=caso_grande)

    pred_pequeno = resp_pequeno.json()["prediction"]
    pred_grande = resp_grande.json()["prediction"]

    # Se o modelo retorna o mesmo valor para inputs extremos, algo esta errado
    assert pred_pequeno != pred_grande
```

**Importante:** esses sao testes de **sanidade**, nao provas de correcao. Eles detectam problemas grosseiros (modelo que retorna constante, features na ordem errada).

---

## Bloco 6 -- Debugging de pipelines

### Por que pipelines falham de formas inesperadas

O pipeline roda em uma **maquina limpa**: sem historico, sem estado, sem os arquivos da sua maquina. Isso expoe:

* Dependencias instaladas globalmente mas nao no `requirements.txt`
* Arquivos que existem localmente mas nao foram commitados
* Variaveis de ambiente definidas so na sua maquina
* Caminhos que funcionam no Windows mas nao no Linux (o runner e Ubuntu)

### Como ler um log de pipeline

**Heuristica:** va direto ao **step que falhou** e leia o erro **de baixo para cima**.

A ultima mensagem de erro geralmente e a mais informativa. Mas nem sempre -- as vezes o erro visivel e consequencia de algo anterior.

### FAILED vs ERROR no pytest

| Tipo | Significado | Exemplo |
|------|-------------|---------|
| **FAILED** | O teste rodou, mas um `assert` nao passou | `assert 200 == 422` |
| **ERROR** | O teste nem chegou a executar (erro de import, fixture quebrada) | `ModuleNotFoundError` |

**Diferenca pratica:**
* FAILED = seu teste encontrou um bug na API
* ERROR = seu teste tem um problema de configuracao

### Mapa de falhas comuns

| Sintoma no log | Causa provavel | Solucao |
|----------------|----------------|---------|
| `ModuleNotFoundError: No module named 'X'` | Falta no `requirements.txt` | Adicionar ao arquivo |
| `ImportError: cannot import name 'X' from 'Y'` | Versao incompativel | Fixar versao no requirements |
| `FileNotFoundError` | Arquivo nao commitado ou caminho errado | `git add` + verificar caminho |
| `AssertionError: assert 200 == 422` | A API nao rejeitou input invalido | Verificar validacao no Pydantic |
| `ConnectionError` / `Connection refused` | API nao subiu a tempo | Verificar step de inicializacao |
| `KeyError` na resposta JSON | Campo renomeado ou removido | Verificar schema da rota |
| Token vazio (`***` nos logs) | Secret com nome errado | Verificar `secrets.HF_TOKEN` (com s) |

### Reproduzindo falhas localmente

O ciclo editar > push > esperar > ver erro e lento. Reproduza localmente:

```bash
# 1. Crie um ambiente virtual limpo
python -m venv venv_ci
source venv_ci/bin/activate  # ou venv_ci\Scripts\activate no Windows

# 2. Instale APENAS o que esta no requirements.txt
pip install -r requirements.txt

# 3. Rode os testes
pytest tests/ -v --tb=short

# 4. Se algo falha aqui, vai falhar no CI tambem
```

**Se o teste passa no seu ambiente normal mas falha no venv limpo:** falta uma dependencia no `requirements.txt`.

### continue-on-error e if: failure()

As vezes voce quer que o pipeline continue apos falha para coletar mais informacoes:

```yaml
- name: Rodar testes
  run: pytest tests/ -v --tb=short
  continue-on-error: true   # pipeline continua mesmo se falhar

- name: Salvar log de falhas
  if: failure()              # so roda se algo anterior falhou
  run: pytest tests/ -v --tb=long > log_falhas.txt 2>&1
```

### Step de diagnostico

Adicione ao inicio do pipeline para facilitar debugging:

```yaml
- name: Diagnostico do ambiente
  run: |
    echo "=== Python ==="
    python --version
    echo "=== Dependencias instaladas ==="
    pip list
    echo "=== Estrutura do projeto ==="
    find . -type f -name "*.py" | head -20
    echo "=== Variaveis de ambiente ==="
    env | grep -i "hf\|token\|python" | sed 's/=.*/=***/'
```

### Exercicios do Bloco 6

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **6.1** | Essencial | Interpretar um log de falha, distinguir ERROR de FAILED |
| **6.2** | Essencial | Identificar erros objetivos e riscos em um workflow |
| **6.3** | Essencial | Reproduzir uma falha localmente em venv limpo |
| **6.4** | Recomendado | Adicionar step de diagnostico ao pipeline |
| **6.5** | Desafio | Montar o pipeline definitivo com 3 jobs |

### O pipeline definitivo (exercicio 6.5)

O workflow final do Bella Tavola deve ter 3 jobs:

```
Job 1: qualidade
  - Formatacao (black --check)
  - Imports (autoflake --check)
  - Testes smoke (pytest -m smoke)
  Roda em: todo push e PR

Job 2: integracao (needs: qualidade)
  - Baixa modelo do Hub (com secret)
  - Testes de integracao (pytest -m integracao)
  - Cache do modelo
  Roda em: apenas push para main

Job 3: relatorio (needs: integracao, always())
  - Resumo do que passou/falhou
  Roda em: sempre (mesmo se jobs anteriores falharem)
```

Veja o [exemplo completo](../exemplos-workflows/ci-completo.yml) para referencia.

---

## Checklist da Parte 3

Ao final, voce deve conseguir:

* [ ] Criar e configurar um secret no GitHub
* [ ] Usar `${{ secrets.HF_TOKEN }}` corretamente
* [ ] Verificar que o token esta disponivel sem expo-lo nos logs
* [ ] Baixar e carregar o modelo do Hub dentro de um teste
* [ ] Testar o endpoint `/ml/predict` com TestClient
* [ ] Adicionar cache do Hugging Face ao pipeline
* [ ] Identificar qual step falhou em um log
* [ ] Distinguir ERROR de FAILED no pytest
* [ ] Localizar causa raiz lendo o log
* [ ] Reproduzir falha localmente em ambiente limpo
* [ ] Montar o pipeline completo com 3 jobs

---

## Checklist final -- Semana 3 completa

**Parte 1:** Explicar CI/CD, escrever workflow YAML, primeiro pipeline verde.

**Parte 2:** Testes com TestClient, fixtures, parametrize, marcadores.

**Parte 3:** Secrets, modelo no CI, cache, debugging, pipeline completo.

Se voce consegue marcar todos os itens acima, voce domina CI com GitHub Actions para projetos de ML.

---

**Anterior:** [Parte 2 -- Testes automatizados com pytest](parte-2-testes-pytest.md)
