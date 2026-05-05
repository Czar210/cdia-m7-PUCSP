# Parte 1 -- Fundamentos de CI e GitHub Actions

> **Notebook correspondente:** `notebooks/CDIA_CD2_2026_e04_p01_github_actions.ipynb`
>
> **O que voce constroi nesta parte:** Seu primeiro pipeline de CI verde no GitHub Actions.

---

## Bloco 1 -- Por que CI/CD existe

### O problema que CI resolve

Imagine tres pessoas trabalhando no mesmo projeto. Uma altera rotas, outra muda modelos Pydantic, outra adiciona o endpoint `/predict`. No final do dia, tudo e integrado. A API quebra. Mas qual mudanca causou o problema?

Sem automacao, a resposta e: **ninguem sabe ate alguem investigar manualmente.**

CI resolve isso automatizando a verificacao a cada commit. Se algo quebrou, voce sabe exatamente quando e em qual mudanca.

### CI -- Integracao Continua

**Definicao:** Integrar mudancas de codigo com frequencia e verificar automaticamente se a integracao nao quebrou nada.

**Na pratica, isso significa:**
* A cada push ou pull request, um **pipeline** roda automaticamente
* O pipeline executa uma sequencia de etapas (instalar dependencias, rodar testes, verificar formatacao)
* Se qualquer etapa falha, o pipeline fica vermelho e voce e notificado

**O pipeline tipico de CI:**
```
Commit/Push --> Instalar deps --> Rodar linter --> Rodar testes --> Resultado (verde/vermelho)
```

### CD -- Entrega e Implantacao Continua

CD tem dois significados relacionados:

| Conceito | O que faz | Quem decide quando vai pro ar |
|----------|-----------|-------------------------------|
| **Entrega Continua** (Continuous Delivery) | Apos CI passar, o codigo esta empacotado e pronto | Um humano aprova |
| **Implantacao Continua** (Continuous Deployment) | Apos CI passar, vai automaticamente para producao | Ninguem -- e automatico |

**Neste projeto, focamos em CI.** CD fica para etapas futuras.

### Por que CI e especialmente importante em ML

Em projetos tradicionais, uma mudanca no codigo quebra uma funcionalidade. Em ML, uma mudanca pode:

* Alterar **silenciosamente** o formato esperado pelo modelo
* Mudar a **ordem das features** e gerar predicoes erradas sem erro aparente
* Fazer o carregamento do modelo falhar apenas em producao
* Quebrar a rota da API de predicao sem afetar as outras

O ponto-chave: em ML, o codigo pode "funcionar" (sem erros) mas produzir **resultados errados**. CI com bons testes detecta isso.

### Exercicios do Bloco 1

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **1.1** | Essencial | Listar 6+ situacoes em que mudancas podem quebrar algo silenciosamente |
| **1.2** | Essencial | Classificar praticas reais como CI, CD (Entrega) ou CD (Implantacao) |

**Dica para o 1.1:** Pense nas fronteiras -- entre a API e o modelo, entre o schema e os dados, entre o que o cliente envia e o que o servidor espera.

---

## Bloco 2 -- YAML e Anatomia de Workflows

### YAML em 5 minutos

YAML e o formato que o GitHub Actions usa para descrever pipelines. As regras fundamentais:

**1. Indentacao define hierarquia (sempre espacos, nunca tabs):**
```yaml
nivel_1:
  nivel_2:
    nivel_3: valor
```

**2. Listas usam hifen:**
```yaml
frutas:
  - maca
  - banana
  - laranja
```

**3. Mapeamentos usam chave: valor:**
```yaml
pessoa:
  nome: "Maria"
  idade: 25
```

**4. Tipos de dados:**
```yaml
texto: "Bella Tavola"        # string
numero: 42                   # int
decimal: 3.14                # float
booleano: true               # bool
nulo: null                   # null
lista_inline: [a, b, c]      # lista em uma linha
```

> Para uma referencia completa, veja [referencia-yaml.md](referencia-yaml.md).

### Anatomia de um workflow

Um workflow e um arquivo `.yml` dentro de `.github/workflows/`. Tem 4 partes:

```yaml
# 1. NOME -- aparece na aba Actions do GitHub
name: CI Pipeline

# 2. GATILHOS -- quando este workflow roda
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# 3. JOBS -- grupos de etapas que rodam em maquinas separadas
jobs:
  verificar-api:
    # 4. RUNNER -- em qual maquina roda
    runs-on: ubuntu-latest

    # STEPS -- as etapas dentro do job
    steps:
      - name: Baixar o codigo
        uses: actions/checkout@v4      # action pronta

      - name: Instalar dependencias
        run: pip install -r requirements.txt   # comando shell
```

### Entendendo cada parte

#### Gatilhos (`on`)

```yaml
on:
  push:                    # roda quando alguem faz push
    branches: [main]       # apenas no branch main

  pull_request:            # roda quando um PR e aberto ou atualizado
    branches: [main]       # apenas em PRs para main

  workflow_dispatch:       # permite rodar manualmente pela interface
```

**Ponto importante:** `pull_request` + `branches: [main]` significa PRs **direcionados** a main, nao PRs **vindos** de main.

#### Jobs e dependencias

Por padrao, jobs rodam em **paralelo**. Para forcar sequencia, use `needs`:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: build          # so comeca depois que 'build' terminar
    steps: [...]
```

#### Steps -- `uses` vs `run`

| Tipo | O que faz | Quando usar |
|------|-----------|-------------|
| `uses` | Usa uma action pronta do marketplace | Tarefas comuns (checkout, setup-python) |
| `run` | Executa comando shell | Seus comandos especificos |

```yaml
steps:
  - name: Baixar o codigo
    uses: actions/checkout@v4          # action pronta

  - name: Instalar dependencias
    run: pip install -r requirements.txt   # comando shell

  - name: Varios comandos
    run: |                             # pipe para multiplas linhas
      echo "Verificando..."
      python -m pytest tests/
```

#### O runner

O runner e a maquina virtual onde o pipeline roda:

| Runner | Sistema |
|--------|---------|
| `ubuntu-latest` | Linux (Ubuntu) -- **use este** |
| `windows-latest` | Windows |
| `macos-latest` | macOS |

Para projetos Python, `ubuntu-latest` e a escolha padrao.

### Exercicios do Bloco 2

| Exercicio | Nivel | O que voce faz |
|-----------|-------|----------------|
| **2.1** | Essencial | Ler um workflow e explicar cada componente |
| **2.2** | Essencial | Encontrar e corrigir 4 erros em um YAML invalido |
| **2.3** | Essencial | **Escrever seu primeiro workflow e ve-lo ficar verde** |
| **2.4** | Desafio | Refatorar para multiplos jobs com `needs` |

### Como fazer o exercicio 2.3 (passo a passo)

Este e o exercicio mais importante da Parte 1. Passo a passo:

1. **Confirme que a API roda localmente:**
   ```bash
   uvicorn main:app --reload
   # Em outro terminal:
   curl http://localhost:8000/
   ```

2. **Crie o arquivo de workflow:**
   ```
   .github/workflows/ci.yml
   ```

3. **Escreva o workflow minimo** (veja o [exemplo basico](../exemplos-workflows/ci-basico.yml))

4. **Faca commit e push:**
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "ci: adiciona pipeline basico"
   git push
   ```

5. **Abra a aba Actions no GitHub** e acompanhe a execucao

6. **Se falhar:** leia o log do step que falhou. Os erros mais comuns:

   | Mensagem | Causa |
   |----------|-------|
   | `ModuleNotFoundError: No module named 'fastapi'` | `requirements.txt` incompleto |
   | `No such file or directory: 'main.py'` | Nome do arquivo principal diferente |
   | `Connection refused` | A API nao subiu a tempo |

### Erros comuns de YAML

| Erro | Exemplo | Correcao |
|------|---------|----------|
| Tab ao inves de espaco | Indentacao com tab | Use apenas espacos (2 ou 4) |
| Indentacao errada | `runs-on` fora do job | Indente dentro do job |
| `with` sem indentar parametros | `python-version` no mesmo nivel de `with` | Indente dentro de `with` |
| String nao citada com `:` | `name: CI: Pipeline` | Use aspas: `name: "CI: Pipeline"` |

---

## Checklist da Parte 1

Ao final, voce deve conseguir:

* [ ] Explicar CI vs CD (Entrega) vs CD (Implantacao)
* [ ] Identificar situacoes em que mudancas quebram algo silenciosamente
* [ ] Explicar `uses` vs `run` em um step
* [ ] Identificar os 4 componentes de um workflow (name, on, jobs, steps)
* [ ] Escrever um workflow do zero
* [ ] Fazer o pipeline ficar verde na aba Actions
* [ ] Ler o log quando algo falha e identificar a causa

---

**Proximo:** [Parte 2 -- Testes automatizados com pytest](parte-2-testes-pytest.md)
