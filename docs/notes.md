# Notas por Módulo, FastAPI (Bella Tavola)

## Visão geral

Este repositório contém um caderno didático que guia pela construção de uma API com FastAPI, cobrindo:
* Bloco 1, Surface: rotas, parâmetros e modelos Pydantic
* Bloco 2, Robustez: tratamento de erros, validação e regras de negócio
* Bloco 3, Estrutura: routers, models, configurações e organização do projeto

As notas abaixo sintetizam sintaxe, boas práticas, padrões de negócio e lógica apresentada em cada bloco.

---

## Bloco 1, Surface (rotas, parâmetros, modelos)

Principais conceitos:
* Definir app: `app = FastAPI(title="...", version="...")`
* Rotas: `@app.get("/caminho")`, `@app.post(...)`, `@app.put(...)`, `@app.delete(...)`.
* Path params: `@app.get("/pratos/{id}")`, tipar o parâmetro (`id: int`).
* Query params: parâmetros opcionais na função com valores padrão (`categoria: Optional[str] = None`).
* Request body com Pydantic: criar classes `BaseModel` e usá-las como parâmetros de função.

Sintaxe exemplificada:
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Prato(BaseModel):
    nome: str
    preco: float

@app.post('/pratos')
async def criar_prato(prato: Prato):
    return {"id": 1, **prato.model_dump()}
```

Boas práticas do Bloco 1:
* Use `response_model` para documentar e filtrar campos retornados (evita vazar dados internos).
* Valide tipos e formas com Pydantic para reduzir checagens manuais.
* Mantenha rotas simples: uma responsabilidade por rota.
* Use query params para filtros combináveis (categoria, preco_maximo, disponivel).

Padrões de negócio e lógica:
* Identificar recursos por ID (path parameter).
* Manter dados em memória para exercícios; persista em DB em produção.
* Ao criar recursos, gere `id` unicamente e retorne `201 Created`.

Pitfalls comuns:
* Retornar mensagens de erro com status 200 (problema abordado no Bloco 2).
* Não usar `response_model` pode expor campos indesejados.

---

## Bloco 2, Robustez (erros, validação, regras de negócio)

Principais conceitos:
* `HTTPException(status_code=..., detail=...)` para erros semanticamente corretos.
* `RequestValidationError` tratado por `@app.exception_handler` para formato consistente.
* `Field` e `field_validator` do Pydantic para validar limites, padrões e regras complexas.

Sintaxe e exemplos:
```python
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator

class PratoInput(BaseModel):
    nome: str = Field(min_length=3)
    preco: float = Field(gt=0)

    @field_validator('preco_promocional')
    @classmethod
    def validar_promocao(cls, v, info):
        # lógica de negócio: desconto não maior que 50%
        return v

raise HTTPException(status_code=404, detail='Prato não encontrado')
```

Boas práticas do Bloco 2:
* Sempre retornar códigos HTTP corretos (404 para não encontrado, 400 para bad request de negócio, 422 para validação).
* Unificar formato de erro com `exception_handler` para facilitar clientes (campos: `erro`, `status`, `path`, `detalhes`).
* Validar regras de negócio dentro de validadores quando for relacionado à estrutura dos dados; use checagens na rota para estado atual (ex.: disponibilidade).

Padrões de negócio e lógica:
* Diferenciar `estructural` (tipo e presença de campos) vs `negócio` (regras como desconto máximo).
* Validações de entrada: `Field` para limites simples, `field_validator` para regras que relacionam campos.

Pitfalls comuns:
* Confluir validação de tipo com regras de negócio, trate ambos, mas com mensagens e códigos distintos.
* Não padronizar erro dificulta tratamento cliente.

---

## Bloco 3, Estrutura (routers, models, config)

Principais conceitos:
* `APIRouter` para agrupar rotas por domínio (`routers/pratos.py` etc.).
* Separar modelos em `models/` para evitar importações circulares e reutilizar schemas.
* `pydantic_settings.BaseSettings` (ou `pydantic-settings`) para configurações via `.env`.

Sintaxe e exemplo de router:
```python
from fastapi import APIRouter
router = APIRouter()

@router.get('/')
async def listar():
    return []

# main.py
app.include_router(router, prefix='/pratos', tags=['Pratos'])
```

Boas práticas do Bloco 3:
* Organização: `routers/`, `models/`, `config.py` e `main.py` enxuto.
* Use `response_model` nos routers para manter contratos.
* Use `settings = BaseSettings()` para configurar limites (ex.: `max_mesas`) e referencie em `models` para validação.
* Crie `__init__.py` em `routers/` e `models/` para pacotes.

Padrões de negócio e lógica:
* Validar limites configuráveis usando `settings` (ex.: número máximo de pessoas por mesa).
* Evitar estado global mutável em produção, use DB/transações; o estado em memória é apenas para exercícios.

Testes e verificação rápida:
* O `tests/run_tests.py` faz verificações de fluxo básico: root, listagem, validação 422, criação 201, presença na lista, 404 e erro de negócio (400). Use-o como smoke tests locais.

Recomendações finais:
* Modularize cedo: mesmo para projetos pequenos, separar routers/models facilita colaboração.
* Padronize erros e schemas para que clientes possam confiar no contrato.
* Escreva testes automatizados pequenos para fluxos críticos (criar → listar → buscar → erros esperados).
