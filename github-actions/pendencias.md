# Pendencias para o projeto funcionar

> Resolva na ordem. Cada bloco desbloqueia uma fase do projeto.
> Status do que ja existe na pasta `Hug/`: gerador de dados (OK), treino de modelo (OK), modelos .pkl locais (OK).
> Status do que ja existe na pasta `Fast-API/`: API com rotas de pratos/bebidas/pedidos/reservas (parcial -- main.py quebrado).

---

## Fase 1 -- API funcionando (desbloqueia Partes 1 e 2 do CI)

- [ ] **Arrumar o `Fast-API/main.py`** -- o arquivo esta quebrado: tem modelos Pydantic duplicados (definidos no main.py E importados de `models/`), e os imports de routers estao dentro do exception handler. Limpar e deixar so os imports dos modulos `models/` e `routers/`.
- [ ] **Adicionar dependencias ao `Fast-API/requirements.txt`** -- faltam: `httpx`, `pytest`, `pydantic-settings`, `scikit-learn`, `joblib`, `huggingface_hub`. Hoje so tem: fastapi, uvicorn, pydantic, requests, faker, pandas, numpy.
- [ ] **Testar a API localmente** -- rodar `uvicorn main:app --reload` na pasta `Fast-API/` e confirmar que `curl http://localhost:8000/` retorna 200.
- [ ] **Confirmar que as rotas principais respondem** -- testar GET `/pratos`, GET `/bebidas`, POST `/pratos`, POST `/pedidos`.

## Fase 2 -- Dados sinteticos e modelo treinado (Caderno 3, Blocos 1-2)

> A pasta `Hug/` ja tem `generator.py` com geradores de credit/churn/fraud e `train_and_save.py` que treina RandomForest. Modelos .pkl ja existem em `Hug/data/models/`. Verifique o que ja esta feito antes de refazer.

- [ ] **Confirmar que o gerador funciona** -- rodar `python -m Hug` na raiz do repo e ver se gera dados em `Hug/data/`.
- [ ] **Escolher o dominio do time** -- credit, churn ou fraud. O `generator.py` ja tem geradores para os tres.
- [ ] **Confirmar que o modelo treina e serializa** -- rodar `python -m Hug.train_and_save` e ver se gera os .pkl em `Hug/data/models/`.
- [ ] **Validar ciclo salvar/carregar** -- carregar o .pkl com `joblib.load()` e confirmar que `model.predict()` funciona com um array de teste.

## Fase 3 -- Publicar no Hugging Face Hub (Caderno 3, Bloco 3)

- [x] **Criar conta no Hugging Face** -- ja tem conta.
- [x] **Gerar token de acesso** -- token ja existe em `.env.local` (comeca com `hf_...`).
- [ ] **Criar repositorio no Hub** -- usar `huggingface_hub` ou interface web. Convencao: `seu-usuario/mlops-[dominio]-v1` (ex: `seu-usuario/mlops-credit-v1`).
- [ ] **Escrever o model card (README.md)** -- documentar: para que serve, features, metricas reais do classification_report, limitacoes. Nao deixar valores como "XX".
- [ ] **Fazer upload dos artefatos** -- publicar `model.pkl`, `README.md` e `requirements.txt` (com versoes de sklearn/joblib/numpy) no repositorio do Hub.
- [ ] **Verificar no navegador** -- abrir o repo no Hub e confirmar: README renderizado, model.pkl listado, requirements.txt presente.

## Fase 4 -- Integrar modelo a API (Caderno 3, Bloco 4)

- [ ] **Implementar `model_utils.py`** -- criar na pasta `Fast-API/` (nao na `Hug/`) com a funcao `load_model(repo_id, filename="model.pkl", force_download=False)` que usa `hf_hub_download` + `joblib.load`. O arquivo em `Hug/model_utils.py` esta vazio -- precisa ser implementado tambem ou apenas na Fast-API.
- [ ] **Implementar `routers/predict.py`** -- na pasta `Fast-API/routers/`, criar endpoint `POST /predict` que: recebe features via JSON (schema Pydantic), monta array numpy NA MESMA ORDEM do treino, chama model.predict() e model.predict_proba(), retorna prediction + probability + label.
- [ ] **Implementar `GET /ml/health`** -- endpoint que verifica se o modelo esta carregado e funcional (nao so se a API esta no ar).
- [ ] **Registrar router no main.py** -- adicionar `app.include_router(predict.router, prefix="/ml", tags=["ML"])`.
- [ ] **Configurar `.env` com token** -- preencher `HF_TOKEN=hf_...` no `.env` da Fast-API. O campo `HUGGINGFACE_HUB_TOKEN` ja existe mas esta vazio.
- [ ] **Testar `/ml/predict` localmente** -- abrir Swagger (`/docs`), enviar payload valido, confirmar que retorna predicao. Testar com caso positivo e negativo.
- [ ] **Testar `/ml/health` localmente** -- confirmar que retorna status do modelo.

## Fase 5 -- Testes com pytest (desbloqueia Blocos 3 e 4 do CI)

- [ ] **Criar pasta `tests/` com estrutura pytest** -- hoje `Fast-API/tests/` so tem `run_tests.py` (sem pytest). Criar `tests/conftest.py`, `tests/test_saude.py`, `tests/test_pratos.py`.
- [ ] **Escrever testes basicos (smoke)** -- teste que a API responde, rotas GET retornam 200, POST com dados validos funciona.
- [ ] **Escrever testes de validacao** -- POST com dados invalidos retorna 422, busca por ID inexistente retorna 404.
- [ ] **Escrever testes do modelo** -- `/ml/predict` com payload valido, `/ml/health` retorna status, modelo distingue casos extremos.
- [ ] **Criar `pytest.ini`** -- registrar marcadores: smoke, validacao, integracao.
- [ ] **Rodar `pytest tests/ -v` localmente e ver tudo verde** -- antes de colocar no pipeline.

## Fase 6 -- Pipeline no GitHub Actions (desbloqueia tudo)

- [ ] **Criar o secret `HF_TOKEN` no repositorio GitHub** -- Settings > Secrets and variables > Actions > New repository secret. Valor: o token `hf_...` da Fase 3.
- [ ] **Criar `.github/workflows/ci.yml`** -- usar os exemplos em `exemplos-workflows/` como base. Comecar com o basico, evoluir para o completo.
- [ ] **Push e confirmar pipeline verde** -- primeiro com testes smoke (sem modelo), depois adicionar testes de integracao (com modelo + secret).
- [ ] **Adicionar cache do Hugging Face** -- para nao baixar o modelo a cada execucao.
- [ ] **Montar pipeline definitivo com 3 jobs** -- qualidade > integracao > relatorio (exercicio 6.5).
