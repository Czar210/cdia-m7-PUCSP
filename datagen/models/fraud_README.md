---
language: pt
tags:
  - sklearn
  - classification
  - fraud
  - mlops
---

# mlops-fraud-v1

Modelo RandomForest para classificação binária ,  domínio **fraud**.
Desenvolvido como parte do curso CDIA M7 ,  Semana 3.

## Uso

```python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("Zaras210/mlops-fraud-v1", "model.pkl"))
prediction = model.predict([[...]])
```

## Features de entrada

| Feature | Tipo | Descrição |
|---------|------|-----------|
| amount | float | Valor da transação |
| hour | int | Hora da transação (0-23) |
| num_items | int | Número de itens |
| customer_age | int | Idade do cliente |
| transaction_history_score | int | Score de histórico (0-100) |

**Target:** `is_fraud` (0 = negativo, 1 = positivo)

## Métricas (test set)

| Métrica | Valor |
|---------|-------|
| Accuracy | 0.998 |
| Precision (classe 1) | 1.000 |
| Recall (classe 1) | 0.889 |
| F1-score (classe 1) | 0.941 |

## Limitações

- Treinado com **dados sintéticos** ,  não reflete distribuições reais.
- RandomForest com hiperparâmetros padrão, sem tuning.
- Proporção de classes fixada na geração.
