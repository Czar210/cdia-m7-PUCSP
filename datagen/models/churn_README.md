---
language: pt
tags:
  - sklearn
  - classification
  - churn
  - mlops
---

# mlops-churn-v1

Modelo RandomForest para classificação binária ,  domínio **churn**.
Desenvolvido como parte do curso CDIA M7 ,  Semana 3.

## Uso

```python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("Zaras210/mlops-churn-v1", "model.pkl"))
prediction = model.predict([[...]])
```

## Features de entrada

| Feature | Tipo | Descrição |
|---------|------|-----------|
| dias_sem_login | int | Dias desde o último login |
| num_chamados | int | Número de chamados abertos |
| valor_mensalidade | float | Valor da mensalidade |
| meses_contrato | int | Meses de contrato |
| nps_score | int | Score NPS (0-10) |

**Target:** `churn` (0 = negativo, 1 = positivo)

## Métricas (test set)

| Métrica | Valor |
|---------|-------|
| Accuracy | 1.000 |
| Precision (classe 1) | 1.000 |
| Recall (classe 1) | 1.000 |
| F1-score (classe 1) | 1.000 |

## Limitações

- Treinado com **dados sintéticos** ,  não reflete distribuições reais.
- RandomForest com hiperparâmetros padrão, sem tuning.
- Proporção de classes fixada na geração.
