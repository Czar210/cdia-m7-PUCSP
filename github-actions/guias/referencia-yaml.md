# Referencia rapida -- YAML para GitHub Actions

> Use este documento como cola quando estiver escrevendo ou depurando workflows.

---

## Regras fundamentais

1. **Indentacao com espacos** (nunca tabs). Use 2 espacos por nivel.
2. **Chave: valor** -- sempre tem espaco apos os dois pontos.
3. **Case-sensitive** -- `True` nao e o mesmo que `true`.
4. **Comentarios** com `#`.

---

## Tipos de dados

```yaml
# Strings
nome: "Bella Tavola"
nome_sem_aspas: Bella Tavola     # funciona, mas aspas sao mais seguras

# Numeros
inteiro: 42
decimal: 3.14

# Booleanos
ativo: true
desativado: false

# Nulo
vazio: null

# CUIDADO: estas strings podem ser interpretadas como booleano
# Use aspas para garantir que sao strings:
versao: "3.12"      # sem aspas, 3.12 vira float
on_off: "on"        # sem aspas, 'on' vira true em YAML
```

---

## Estruturas

### Mapeamento (dicionario)

```yaml
pessoa:
  nome: Maria
  idade: 25
  cidade: "Sao Paulo"
```

Equivale a `{"pessoa": {"nome": "Maria", "idade": 25, ...}}` em JSON.

### Lista

```yaml
# Formato expandido
frutas:
  - maca
  - banana
  - laranja

# Formato inline
frutas: [maca, banana, laranja]
```

### Lista de mapeamentos

```yaml
steps:
  - name: Passo 1
    run: echo "oi"

  - name: Passo 2
    run: echo "tchau"
```

---

## Strings multilinha

```yaml
# Literal (|) -- preserva quebras de linha
descricao: |
  Linha 1
  Linha 2
  Linha 3

# Folded (>) -- junta linhas em uma so
descricao: >
  Tudo isso vira
  uma unica linha
  de texto.
```

**No GitHub Actions, use `|` para multiplos comandos:**

```yaml
- name: Varios comandos
  run: |
    echo "Passo 1"
    pip install -r requirements.txt
    pytest tests/ -v
```

---

## Anatomia completa de um workflow

```yaml
# ============================================
# 1. NOME (aparece na aba Actions)
# ============================================
name: CI -- Bella Tavola

# ============================================
# 2. GATILHOS (quando roda)
# ============================================
on:
  push:
    branches: [main]           # push para main
  pull_request:
    branches: [main]           # PR direcionado a main
  workflow_dispatch:            # botao manual na interface

# ============================================
# 3. JOBS (o que roda)
# ============================================
jobs:
  nome-do-job:                  # identificador (sem espacos)
    runs-on: ubuntu-latest      # maquina virtual

    # ========================================
    # 4. STEPS (etapas do job)
    # ========================================
    steps:
      # Action pronta (uses)
      - name: Baixar o codigo
        uses: actions/checkout@v4

      # Comando shell (run)
      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Comando com variavel de ambiente
      - name: Rodar testes
        run: pytest tests/ -v
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
```

---

## Gatilhos comuns

```yaml
on:
  # Push para branches especificos
  push:
    branches: [main, develop]

  # PR para branches especificos
  pull_request:
    branches: [main]

  # Manual (botao na interface)
  workflow_dispatch:

  # Agendado (cron)
  schedule:
    - cron: '0 8 * * 1'    # toda segunda as 8h UTC
```

---

## Jobs -- dependencias e condicoes

```yaml
jobs:
  # Job 1: roda sempre
  qualidade:
    runs-on: ubuntu-latest
    steps: [...]

  # Job 2: so roda se qualidade passou
  testes:
    runs-on: ubuntu-latest
    needs: qualidade
    steps: [...]

  # Job 3: so roda em push (nao em PR)
  deploy:
    runs-on: ubuntu-latest
    needs: testes
    if: github.event_name == 'push'
    steps: [...]

  # Job 4: roda SEMPRE, mesmo se anteriores falharem
  relatorio:
    runs-on: ubuntu-latest
    needs: [qualidade, testes]
    if: always()
    steps: [...]
```

---

## Variaveis e secrets

```yaml
# Variavel de ambiente simples
env:
  AMBIENTE: producao

# Secret (valor protegido)
env:
  HF_TOKEN: ${{ secrets.HF_TOKEN }}

# Variavel do contexto GitHub
env:
  BRANCH: ${{ github.ref_name }}
```

**Regra:** nunca coloque tokens ou senhas diretamente no YAML. Use secrets.

---

## Erros comuns de YAML

| Erro | Problema | Correcao |
|------|----------|----------|
| `runs-on` fora do job | Indentacao errada | Indentar dentro do job |
| `python-version: 3.12` | Interpretado como float | Usar aspas: `"3.12"` |
| Tab ao inves de espaco | YAML invalido | Substituir por espacos |
| `secret.HF_TOKEN` | Falta o `s` | `secrets.HF_TOKEN` |
| `name: CI: Pipeline` | Dois pontos na string | Usar aspas: `"CI: Pipeline"` |
| `with` sem sub-indentacao | Parametros fora do `with` | Indentar dentro de `with` |

---

## Actions mais usadas

| Action | Funcao |
|--------|--------|
| `actions/checkout@v4` | Clona o repositorio |
| `actions/setup-python@v5` | Instala versao do Python |
| `actions/cache@v4` | Cache de dependencias/arquivos |
| `actions/upload-artifact@v4` | Salva arquivos como artefato |
