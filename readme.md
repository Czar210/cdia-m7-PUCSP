# Projeto Bella Tavola

Entrega da Semana 3 da disciplina **CD2** (CDIA M7, PUC-SP, 2026).

Este repositório reúne os 5 cadernos resolvidos do módulo, junto com o código completo de uma API FastAPI integrada a um modelo de Machine Learning publicado no Hugging Face Hub, e um pipeline de Integração Contínua no GitHub Actions.

A API é fictícia (um restaurante chamado Bella Tavola) e serve como cenário comum aos três temas: construção de API, dados sintéticos com modelo de ML, e CI/CD.

## Visão geral da entrega

* API REST em FastAPI com 5 routers, validação Pydantic, exception handler global e configuração via BaseSettings.
* Pacote de geração de dados sintéticos para 3 domínios (crédito, churn, fraude), com treinamento de RandomForest e publicação automática no Hugging Face Hub com model card gerado a partir das métricas reais.
* Endpoint `/ml/predict` integrado ao modelo, com carregamento único na inicialização e fallback para download do Hub.
* 53 testes pytest cobrindo rotas, validação, contratos e comportamento do modelo.
* Pipeline CI no GitHub Actions com 3 jobs (qualidade, integracao, relatorio), uso de secrets e cache do Hugging Face.

## Estrutura do repositório

```
api/                    Código FastAPI (routers, models, tests, config)
datagen/                Geração de dados sintéticos, treino e upload pro Hub
notebooks/              Os 5 cadernos resolvidos
docs/                   Anotações de aula, guias de CI, documentação
data/                   CSVs gerados pelo datagen
.github/workflows/      Pipeline CI (ci.yml)
```

| Pasta | O que contém |
|---|---|
| `api/` | App FastAPI, routers separados por domínio, models Pydantic, suíte de testes |
| `datagen/` | Geradores de dados sintéticos, scripts de treino e upload, modelos `.pkl` |
| `notebooks/` | Os 5 cadernos do curso |
| `docs/` | Anotações, guias de CI, exemplos de workflow, documentação técnica |
| `data/` | Datasets gerados (saída do datagen) |
| `.github/workflows/` | Workflow CI |

## Os 5 cadernos

| Caderno | Tema | Arquivo |
|---|---|---|
| e02 | FastAPI: rotas, validação e organização | `notebooks/CDIA_CD2_2026_e02_fastAPI.ipynb` |
| e03 | Dados sintéticos e Hugging Face Hub | `notebooks/CDIA_CD2_2026_e03_dados_sintéticos.ipynb` |
| e04 p01 | GitHub Actions: fundamentos de CI | `notebooks/CDIA_CD2_2026_e04_p01_github_actions.ipynb` |
| e04 p02 | GitHub Actions: testes com pytest | `notebooks/CDIA_CD2_2026_e04_p02_github_actions.ipynb` |
| e04 p03 | GitHub Actions: integração ML e pipeline completo | `notebooks/CDIA_CD2_2026_e04_p03_github_actions.ipynb` |

## Como rodar

### Requisitos

* Python 3.12
* Conta no Hugging Face (apenas se quiser baixar o modelo do Hub em vez de usar o cache local)

### Instalação

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r api/requirements.txt
```

### Variáveis de ambiente

Crie um `.env` na raiz a partir do exemplo:

```bash
cp api/.env.example .env
```

As variáveis principais são:

| Variável | O que faz |
|---|---|
| `MODEL_PATH` | Caminho do `.pkl` local. Se setado, evita baixar do Hub |
| `HF_TOKEN` | Token do Hugging Face (obrigatório se `MODEL_PATH` não existir) |
| `HF_REPO_ID` | ID do repositório no Hub (default: `Zaras210/mlops-credit-v1`) |
| `RESERVATION_MIN_HOURS` | Antecedência mínima para reservas |

### Subir a API

A partir da pasta `api/`:

```bash
cd api
MODEL_PATH=../datagen/models/credit_rf.pkl uvicorn main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação interativa (Swagger) fica em `http://localhost:8000/docs`.

### Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Saudação |
| GET | `/health` | Status da API e do modelo |
| GET | `/pratos` | Lista pratos com filtros opcionais |
| POST | `/pratos` | Cadastra prato com validação |
| GET | `/bebidas` | Lista bebidas |
| POST | `/pedidos` | Cria pedido |
| POST | `/reservas` | Cria reserva (valida antecedência mínima) |
| POST | `/ml/predict` | Predição de inadimplência |

### Rodar os testes

API (53 testes da API):

```bash
cd api
MODEL_PATH=../datagen/models/credit_rf.pkl python -m pytest tests/ --tb=short
```

Datagen (testes da geração de dados):

```bash
python -m pytest datagen/tests/ --tb=short
```

### Gerar dados e treinar modelos do zero

```bash
python -m datagen                        # gera os datasets sintéticos
python -m datagen.train_and_save         # treina e serializa os 3 modelos
python -m datagen.upload_to_hub --domain credit   # publica no Hub
```

## Pipeline CI

O workflow está em `.github/workflows/ci.yml` e tem 3 jobs:

1. **qualidade**: roda em todo push e Pull Request. Instala dependências, faz diagnóstico do ambiente e executa apenas os testes marcados como `smoke`. Feedback rápido.
2. **integracao**: roda apenas em push para `main`, depois que `qualidade` passa. Configura cache do Hugging Face, valida que `HF_TOKEN` está presente sem expor o valor nos logs, e roda a suíte completa.
3. **relatorio**: imprime o resumo final do pipeline.

A separação por markers (`smoke`, `validacao`, `integracao`, definidos em `api/pytest.ini`) permite que cada job rode um subconjunto distinto da suíte.

## Modelo de ML

O modelo de crédito está publicado em `https://huggingface.co/Zaras210/mlops-credit-v1`.

Features de entrada do `/ml/predict`:

| Campo | Tipo |
|---|---|
| `renda_mensal` | float |
| `divida_atual` | float |
| `historico_pagamentos` | int (0 a 100) |
| `idade` | int |
| `num_dependentes` | int |

Saída: `probability` (float entre 0 e 1) e `label` (`adimplente` ou `inadimplente`).

Exemplo de chamada:

```bash
curl -X POST http://localhost:8000/ml/predict \
  -H "Content-Type: application/json" \
  -d '{"renda_mensal":3000,"divida_atual":1500,"historico_pagamentos":40,"idade":30,"num_dependentes":3}'
```

## Stack

* **API**: FastAPI, Pydantic, pydantic-settings, Uvicorn
* **ML**: scikit-learn (RandomForest), joblib, huggingface_hub
* **Testes**: pytest, httpx (TestClient)
* **CI**: GitHub Actions
* **Dados**: pandas, numpy, faker

## Decisões de arquitetura

Documentadas em `docs/detalhes.md`. Resumindo:

* Separação por responsabilidade: `api/` é só FastAPI, `datagen/` é só geração e treino, `notebooks/` são os cadernos do curso.
* Rotas separadas por domínio em `api/routers/`, cada uma com seu próprio `APIRouter`.
* Models Pydantic isolados em `api/models/`, reaproveitáveis nos testes.
* Configuração via `BaseSettings` lendo do `.env`, sem variáveis hardcoded.
* O carregamento do modelo de ML acontece uma única vez na inicialização da API, com cache em memória.
* O endpoint `/health` distingue claramente "API no ar" de "modelo carregado".

## Autor

César Augusto Sibila, CDIA M7, PUC-SP, 2026.
