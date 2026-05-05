# Lista de Endpoints, Bella Tavola API

Organizado por blocos: Raiz, Pratos, Bebidas.

**Raiz**
* GET `/`, Retorna informações gerais do restaurante (nome, mensagem, chef, cidade, especialidade).

**Pratos**
* GET `/pratos`, Lista pratos.
  * Query params: `categoria` (string, opcional), `preco_maximo` (float, opcional), `disponivel` (bool, opcional)
  * Resposta: lista de objetos prato (`id`, `nome`, `categoria`, `preco`, `ingredientes?`, `disponivel`, ...)

* GET `/pratos/{prato_id}`, Busca prato por `id`.
  * Query params: `disponivel` (bool, opcional), quando fornecido filtra por disponibilidade.
  * 404 se não encontrado ou não corresponder ao filtro.

* GET `/pratos/{prato_id}/detalhes`, Retorna prato; Query param `incluir_ingredientes` (bool, default false) inclui/exclui campo `ingredientes`.

* POST `/pratos/input`, Cria um novo prato (request body: `PratoInput`).
  * `PratoInput` valida com `Field`: `nome` (min_length=3), `categoria` (pattern: pizza|massa|sobremesa|entrada|salada), `preco` (gt=0), `descricao` (opcional), `disponivel` (bool).
  * Retorna 201 e o objeto criado com `id` e `criado_em`.

**Bebidas**
* GET `/bebidas`, Lista bebidas.
  * Query params: `categoria` (string, opcional), `preco_maximo` (float, opcional), `disponivel` (bool, opcional)

* GET `/bebidas/{bebida_id}`, Busca bebida por `id`.
  * Query params: `disponivel` (bool, opcional)

* GET `/bebidas/{bebida_id}/detalhes`, Retorna bebida; Query param `incluir_ingredientes` (bool) inclui/exclui `ingredientes`.

* POST `/bebidas/input`, Cria nova bebida (request body: `BebidaInput`).
  * `BebidaInput` valida com `Field`: `nome` (min_length=3), `categoria` (pattern: vinho|agua|refrigerante|suco|cerveja|drink|digestivo|cafe), `preco` (gt=0), `descricao` (opcional), `disponivel` (bool).
  * Retorna 201 e o objeto criado com `id` e `criado_em`.

Observações rápidas
* As validações são implementadas via `pydantic.Field` em `main.py`, ver [main.py](main.py).
* Testes básicos automáticos foram adicionados e executados (`tests/run_tests.py`) e passaram.
* Se preferir enums em vez de `pattern` para categorias, posso alterar os modelos para `Literal`/`Enum`.

Arquivo de referência do código: [main.py](main.py)
