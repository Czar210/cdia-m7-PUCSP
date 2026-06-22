# Projeto Bella Tavola

Entrega da disciplina **CD2** (CDIA M7, PUC-SP, 2026), consolidando até a Semana 5 (Docker e MLOps).

Este repositório reúne os 8 cadernos resolvidos do módulo, junto com o código completo de uma API FastAPI integrada a um modelo de Machine Learning publicado no Hugging Face Hub, um pipeline de Integração Contínua no GitHub Actions e a containerização da aplicação com Docker (build, orquestração com Compose e publicação automática no Docker Hub).

A API é fictícia (um restaurante chamado Bella Tavola) e serve como cenário comum aos quatro temas: construção de API, dados sintéticos com modelo de ML, CI/CD e Docker.

## Visão geral da entrega

* API REST em FastAPI com 5 routers, validação Pydantic, exception handler global e configuração via BaseSettings.
* Pacote de geração de dados sintéticos para 3 domínios (crédito, churn, fraude), com treinamento de RandomForest e publicação automática no Hugging Face Hub com model card gerado a partir das métricas reais.
* Endpoint `/ml/predict` integrado ao modelo, com carregamento único na inicialização e fallback para download do Hub.
* 53 testes pytest cobrindo rotas, validação, contratos e comportamento do modelo.
* Containerização com Docker: `Dockerfile` multi-stage com usuário não-root, `.dockerignore`, e orquestração de API + PostgreSQL + Nginx via `docker-compose.yml`.
* Pipeline CI no GitHub Actions com 4 jobs (qualidade, integracao, docker, relatorio), uso de secrets, cache do Hugging Face e publicação da imagem no Docker Hub.

## Estrutura do repositório

```
api/                    Código FastAPI (routers, models, tests, config) + Dockerfile e .dockerignore
datagen/                Geração de dados sintéticos, treino e upload pro Hub
notebooks/              Os 8 cadernos resolvidos
docs/                   Anotações de aula, guias de CI, documentação
data/                   CSVs gerados pelo datagen
docker-compose.yml      Orquestra API + PostgreSQL + Nginx
nginx.conf              Configuração do proxy reverso (Nginx)
.github/workflows/      Pipeline CI (ci.yml)
```

| Caminho | O que contém |
|---|---|
| `api/` | App FastAPI, routers por domínio, models Pydantic, suíte de testes, `Dockerfile` e `.dockerignore` |
| `datagen/` | Geradores de dados sintéticos, scripts de treino e upload, modelos `.pkl` |
| `notebooks/` | Os 8 cadernos do curso |
| `docs/` | Anotações, guias de CI, exemplos de workflow, documentação técnica |
| `data/` | Datasets gerados (saída do datagen) |
| `docker-compose.yml` | Orquestração multi-serviço (API, banco, proxy reverso) |
| `nginx.conf` | Proxy reverso na frente da API |
| `.github/workflows/` | Workflow CI |

## Os 8 cadernos

| Caderno | Tema | Arquivo |
|---|---|---|
| e02 | FastAPI: rotas, validação e organização | `notebooks/CDIA_CD2_2026_e02_fastAPI.ipynb` |
| e03 | Dados sintéticos e Hugging Face Hub | `notebooks/CDIA_CD2_2026_e03_dados_sintéticos.ipynb` |
| e04 p01 | GitHub Actions: fundamentos de CI | `notebooks/CDIA_CD2_2026_e04_p01_github_actions.ipynb` |
| e04 p02 | GitHub Actions: testes com pytest | `notebooks/CDIA_CD2_2026_e04_p02_github_actions.ipynb` |
| e04 p03 | GitHub Actions: integração ML e pipeline completo | `notebooks/CDIA_CD2_2026_e04_p03_github_actions.ipynb` |
| e05 p01 | Docker: primeira imagem e Dockerfile da API | `notebooks/CDIA_CD2_2026_e05_p01_docker.ipynb` |
| e05 p02 | Docker: variáveis, volumes, Compose e boas práticas | `notebooks/CDIA_CD2_2026_e05_p02_docker.ipynb` |
| e05 p03 | Docker: build e push da imagem no pipeline de CI | `notebooks/CDIA_CD2_2026_e05_p03_docker.ipynb` |

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

### Rodar com Docker

A imagem é construída a partir de `api/Dockerfile` (multi-stage, usuário não-root). O `.dockerignore` na mesma pasta evita copiar secrets (`.env`), testes, cadernos e o `.pkl` (o modelo é baixado do Hub em runtime).

Build e execução de um contêiner isolado:

```bash
docker build -t bella-tavola:v1 ./api
docker run -p 8000:8000 --rm --env-file .env bella-tavola:v1
# API em http://localhost:8000
```

Sistema completo (API + PostgreSQL + Nginx) via Compose, a partir da raiz do projeto:

```bash
docker compose up -d        # sobe os três serviços em background
curl http://localhost/      # a API responde via Nginx na porta 80
docker compose down         # para tudo (preserva os volumes)
```

Para o `/ml/predict` funcionar dentro do contêiner, o `.env` da raiz precisa ter `HF_TOKEN` e `HF_REPO_ID` (o modelo é baixado do Hugging Face Hub na primeira chamada). O `.env` nunca é commitado nem entra na imagem.

## Pipeline CI

O workflow está em `.github/workflows/ci.yml` e tem 4 jobs (`qualidade → integracao → docker → relatorio`):

1. **qualidade**: roda em todo push e Pull Request. Instala dependências, faz diagnóstico do ambiente e executa apenas os testes marcados como `smoke`. Feedback rápido.
2. **integracao**: roda apenas em push para `main`, depois que `qualidade` passa. Configura cache do Hugging Face, valida que `HF_TOKEN` está presente sem expor o valor nos logs, e roda a suíte completa.
3. **docker**: roda em push após `integracao` passar. Faz build da imagem e push para o Docker Hub, com tag pelo SHA do commit (rastreabilidade) e `latest`, usando cache de layers do GitHub Actions. Código que não passa nos testes nunca chega ao registry. Requer os secrets `DOCKER_USERNAME` e `DOCKER_PASSWORD`.
4. **relatorio**: imprime o resumo final do pipeline, incluindo a tag da imagem publicada.

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
* **CI/CD**: GitHub Actions, Docker Hub
* **Containers**: Docker (multi-stage), Docker Compose, Nginx, PostgreSQL
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
