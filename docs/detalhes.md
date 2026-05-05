# Detalhes das decisões e alterações

Resumo
- Objetivo: organizar o projeto seguindo o Bloco 3 do notebook, mantendo o esqueleto original e garantindo que os testes de fumaça continuem passando.
- Resultado principal: extração dos modelos para `models/`, criação de `routers/`, atualização de `main.py` para incluir routers, e criação de documentação mínima (`to-do.md`, `notes.md`, `detalhes.md`).

Decisões de arquitetura
- Separação de responsabilidades: Pydantic models ficam em `models/` e lógica de rota em `routers/`. Isso facilita testes unitários, reuso e leitura.
- Rotas: cada domínio (pratos, bebidas, pedidos, reservas) usa um `APIRouter` separado e é incluído em `main.py` com `include_router()`.
- Testes: uso de um script de smoke tests (`tests/run_tests.py`) que valida os contratos principais (status code, validação 422, 404, business errors). Testes são a força sanitizadora durante refatorações.

Mudanças realizadas (por arquivo)
- `main.py`
  - Mantido como entrypoint e responsável por configurar handlers globais de erro e montar os routers.
  - Removidas implementações de rota duplicadas e delegadas aos routers.
- `models/` (novo pacote)
  - `prato.py`, `bebida.py`, `pedido.py`, `reserva.py`:
    - Classes `Input` e `Output` quando aplicável.
    - Validators usando `Field` e `field_validator` para regras de formato e tipos.
  - Racional: manter schemas próximos uns aos outros e reutilizáveis entre rotas e testes.
- `routers/` (novo pacote)
  - `pratos.py`, `bebidas.py`, `pedidos.py`, `reservas.py`:
    - Rotas CRUD/operacionais extraídas do `main.py` original e adaptadas para importar os modelos do pacote `models`.
    - Uso de listas em memória como armazenamento temporário (mesma abordagem do notebook/exercício).
- `tests/run_tests.py`
  - Executado após cada grande mudança para garantir não regressões; atualmente retorna "All tests passed".
- `to-do.md` e `notes.md`
  - Documentação leve para acompanhar progresso e decisões de alto nível.

Racional de design e trade-offs
- Por que não usar banco de dados agora: o objetivo do exercício é didático; usar armazenamento em memória mantém o foco nas rotas, validação e contratos.
- Por que não mover validações de negócio para um serviço separado ainda: mantivemos validações básicas no Pydantic e handlers; migrar para camada de serviço seria próximo passo quando adicionarmos persistência ou lógica complexa.

Validações importantes implementadas
- Validações de payload via Pydantic (tipos, campos obrigatórios, formatos).
- Tratamento de `RequestValidationError` e `HTTPException` em `main.py` para resposta consistente.

Pendências recomendadas
- `config.py` + `.env`: criar um `BaseSettings` (Pydantic) para centralizar configurações (porta, limites de mesa, políticas de reserva). Isto torna a app configurável por ambiente.
- Validadores de negócio avançados: por exemplo, reservar com antecedência mínima (1 hora), limitar número de reservas por mesa/horário.
- Persistência: trocar armazenamento em memória por um banco (SQLite para dev) e adaptar os repositórios.
- CI: adicionar GitHub Actions para rodar `tests/run_tests.py` em PRs.

Próximos passos sugeridos (curto prazo)
- Implementar `config.py` e um `.env.example` (posso criar isso agora).
- Adicionar validação de antecedência mínima para reservas em `models/reserva.py`.
- Subir um workflow de CI que execute `tests/run_tests.py`.

Onde procurar as partes alteradas
- Entrypoint: `Fast-API/main.py`
- Models: `Fast-API/models/`
- Routers: `Fast-API/routers/`
- Tests: `Fast-API/tests/run_tests.py`
- Documentação: `Fast-API/to-do.md`, `Fast-API/notes.md`, `Fast-API/detalhes.md` (este arquivo)

Observações finais
- Mantive o estilo e contratos já presentes no notebook e no `main.py` original para minimizar surpresas para correção manual posterior.
- Se quiser, aplico agora as pendências na ordem: 1) `config.py` + `.env.example`, 2) validação de reservas, 3) persistência.
