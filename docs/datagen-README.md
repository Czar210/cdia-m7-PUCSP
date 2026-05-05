# Hug ,  Synthetic Data Generators

Pacote para gerar datasets sintéticos de classificação usados nos notebooks do curso.

## Domínios disponíveis

| Domínio | Target | Features |
|---------|--------|----------|
| credit  | `inadimplente` | renda_mensal, divida_atual, historico_pagamentos, idade, num_dependentes |
| churn   | `churn` | dias_sem_login, num_chamados, valor_mensalidade, meses_contrato, nps_score |
| fraud   | `is_fraud` | amount, hour, num_items, customer_age, transaction_history_score |

## Uso via CLI

```bash
python -m Hug
```

Gera os 3 datasets em `./data/` (configurável via `HUG_OUTPUT_DIR`).

## Uso via Python

```python
from Hug.generator import generate_credit, generate_churn, generate_fraud

df, X, y = generate_credit(n_samples=2000, seed=42, proporcao_positivos=0.3)
df, X, y = generate_churn(n_samples=1000, seed=42)
df, X, y = generate_fraud(n_samples=5000, seed=42, proporcao_positivos=0.02)
```

## Treinar modelo

```python
from Hug.train_and_save import train_on_domain

result = train_on_domain("credit", n_samples=2000, seed=42)
# Salva modelo .pkl, métricas .json e relatório .txt em Hug/data/models/
```

## Variáveis de ambiente

| Variável | Default | Descrição |
|----------|---------|-----------|
| `HUG_OUTPUT_DIR` | `./data` | Diretório de saída dos CSVs |
| `HUG_SEED` | `42` | Seed para reprodutibilidade |
