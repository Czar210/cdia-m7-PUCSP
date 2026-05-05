# CI com GitHub Actions -- Bella Tavola

## Guia Geral de Aprendizagem

---

## O que voce vai aprender

Este projeto te leva do zero ao pipeline de CI completo para uma API de ML (Bella Tavola). Ao final, voce tera automatizado testes, integracao com modelo e diagnostico de falhas -- tudo rodando a cada commit no GitHub.

**O projeto esta dividido em 3 partes progressivas, cada uma com 2 blocos:**

| Parte | Tema | Blocos | O que voce constroi |
|-------|------|--------|---------------------|
| **1** | Fundamentos de CI e GitHub Actions | 1 e 2 | Primeiro pipeline verde no GitHub |
| **2** | Testes automatizados com pytest | 3 e 4 | Suite de testes real contra a API |
| **3** | Integracao com modelo e debugging | 5 e 6 | Pipeline completo com modelo do HF Hub |

---

## Estrutura do projeto

```
github-actions/
├── guia.md                          <-- voce esta aqui
├── notebooks/
│   ├── ...p01_github_actions.ipynb   <-- Parte 1: Fundamentos
│   ├── ...p02_github_actions.ipynb   <-- Parte 2: Testes
│   └── ...p03_github_actions.ipynb   <-- Parte 3: Integracao + Debug
├── guias/
│   ├── parte-1-fundamentos-ci.md     <-- Guia detalhado da Parte 1
│   ├── parte-2-testes-pytest.md      <-- Guia detalhado da Parte 2
│   ├── parte-3-integracao-debug.md   <-- Guia detalhado da Parte 3
│   ├── referencia-yaml.md            <-- Referencia rapida de YAML
│   └── referencia-pytest.md          <-- Referencia rapida de pytest
├── exemplos-workflows/
│   ├── ci-basico.yml                 <-- Workflow minimo funcional
│   ├── ci-com-testes.yml             <-- Workflow com pytest
│   └── ci-completo.yml               <-- Workflow final com 3 jobs
├── tests/                            <-- Seus testes vao aqui
│   └── (conftest.py, test_*.py)
└── .github/
    └── workflows/
        └── ci.yml                    <-- Seu pipeline real
```

---

## Pre-requisitos

Antes de comecar, confirme que voce tem:

* [ ] API do Bella Tavola funcionando localmente (`uvicorn main:app --reload`)
* [ ] Modelo publicado no Hugging Face Hub (Semana 2)
* [ ] Conta no GitHub com o projeto em um repositorio
* [ ] Git configurado localmente
* [ ] Python com `pip` funcionando
* [ ] `httpx` e `pytest` instalados (ou no `requirements.txt`)

---

## Roteiro passo a passo

### Fase 1: Entender o "por que" (Parte 1, Bloco 1)

**Objetivo:** Antes de escrever qualquer YAML, entender por que CI existe.

1. Leia o notebook da Parte 1, secoes do Bloco 1
2. Leia o [guia detalhado da Parte 1](guias/parte-1-fundamentos-ci.md) -- secao "Bloco 1"
3. Faca os exercicios 1.1 e 1.2 no notebook
4. **Checkpoint:** voce consegue explicar CI vs CD com suas palavras?

### Fase 2: Escrever o primeiro pipeline (Parte 1, Bloco 2)

**Objetivo:** Dominar YAML e colocar o primeiro workflow no ar.

1. Leia a [referencia YAML](guias/referencia-yaml.md) se precisar de apoio com a sintaxe
2. Leia o guia da Parte 1 -- secao "Bloco 2"
3. Estude o [exemplo de workflow basico](exemplos-workflows/ci-basico.yml)
4. Faca os exercicios 2.1 a 2.3 -- o 2.3 e o mais importante: **seu primeiro pipeline verde**
5. Se quiser ir alem, faca o 2.4 (multiplos jobs)
6. **Checkpoint:** seu pipeline esta verde na aba Actions do GitHub?

### Fase 3: Escrever testes reais (Parte 2, Bloco 3)

**Objetivo:** Substituir `curl` por testes automatizados com pytest.

1. Leia o guia da Parte 2 -- secao "Bloco 3"
2. Crie a pasta `tests/` e o primeiro arquivo `test_saude.py`
3. Faca os exercicios 3.1 a 3.4 no notebook
4. Estude o [exemplo de workflow com testes](exemplos-workflows/ci-com-testes.yml)
5. **Checkpoint:** `pytest tests/ -v` passa localmente E no pipeline?

### Fase 4: Melhorar a qualidade dos testes (Parte 2, Bloco 4)

**Objetivo:** Escrever testes robustos, isolados e organizados.

1. Leia o guia da Parte 2 -- secao "Bloco 4"
2. Consulte a [referencia pytest](guias/referencia-pytest.md) para fixtures e parametrize
3. Crie o `conftest.py` (exercicio 4.1)
4. Reescreva testes frageis (exercicio 4.2)
5. Explore parametrizacao e marcadores (exercicios 4.3 e 4.4)
6. **Checkpoint:** seus testes usam fixtures do conftest.py e nao dependem de estado global?

### Fase 5: Integrar o modelo de ML (Parte 3, Bloco 5)

**Objetivo:** O pipeline agora tambem testa o modelo do Hugging Face Hub.

1. Leia o guia da Parte 3 -- secao "Bloco 5"
2. Configure o secret `HF_TOKEN` no repositorio GitHub
3. Faca os exercicios 5.1 a 5.3 (secret, modelo, endpoint /ml/predict)
4. Estude o [exemplo de workflow completo](exemplos-workflows/ci-completo.yml)
5. **Checkpoint:** o pipeline baixa o modelo do Hub e roda testes de integracao?

### Fase 6: Aprender a depurar (Parte 3, Bloco 6)

**Objetivo:** Diagnosticar qualquer falha em pipeline sem adivinhar.

1. Leia o guia da Parte 3 -- secao "Bloco 6"
2. Faca os exercicios 6.1 a 6.3 (leitura de logs, diagnostico, reproducao local)
3. Monte o pipeline definitivo (exercicio 6.5 -- desafio final)
4. **Checkpoint:** voce sabe ler um log de falha e encontrar a causa raiz?

---

## Niveis de dificuldade

Cada exercicio nos notebooks tem um nivel:

| Nivel | Significado | Recomendacao |
|-------|-------------|--------------|
| **Essencial** | Minimo para completar a etapa | Faca todos |
| **Recomendado** | Amplia a qualidade da solucao | Faca se tiver tempo |
| **Desafio** | Aprofunda do ponto de vista de engenharia | Faca para ir alem |

**Sugestao de abordagem:** faca todos os essenciais primeiro, depois volte nos recomendados. Os desafios sao para quem quer aprofundar.

---

## Mapa mental do pipeline final

```
Push ou PR para main
        |
  +-------------+
  |  qualidade  |  --> formatacao + imports + testes smoke
  +------+------+
         | (so em push para main)
         v
  +-------------+
  | integracao  |  --> baixa modelo do Hub + testes de integracao
  +------+------+
         |
         v
  +-------------+
  |  relatorio  |  --> resumo do que passou/falhou
  +-------------+
```

---

## Dicas gerais

1. **Teste localmente antes de fazer push.** O ciclo editar-push-esperar e lento. Rode `pytest tests/ -v` antes.
2. **Leia o log de baixo para cima.** Quando um step falha, a ultima mensagem de erro geralmente e a mais informativa.
3. **O `requirements.txt` e a fonte de verdade.** Se funciona na sua maquina mas nao no CI, provavelmente falta uma dependencia no arquivo.
4. **Commits pequenos e frequentes.** Facilita identificar qual mudanca quebrou o pipeline.
5. **Nao tenha medo de errar.** O pipeline vai quebrar varias vezes -- isso e parte do aprendizado.

---

## Guias detalhados

* [Parte 1 -- Fundamentos de CI e GitHub Actions](guias/parte-1-fundamentos-ci.md)
* [Parte 2 -- Testes automatizados com pytest](guias/parte-2-testes-pytest.md)
* [Parte 3 -- Integracao com modelo e debugging](guias/parte-3-integracao-debug.md)
* [Referencia YAML](guias/referencia-yaml.md)
* [Referencia pytest](guias/referencia-pytest.md)
