---
language: pt
tags:
  * sklearn
  * classification
  * credit
  * mlops
---

# mlops-credit-v1

Modelo RandomForest para classificação binária, domínio **credit**.
Desenvolvido como parte do curso CDIA M7, Semana 3.

## Uso

```python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("Zaras210/mlops-credit-v1", "model.pkl"))
prediction = model.predict([[...]])
```

## Features de entrada

| Feature | Tipo | Descrição |
|---------|------|-----------|
| renda_mensal | float | Renda mensal em reais |
| divida_atual | float | Dívida atual em reais |
| historico_pagamentos | int | Score de histórico (0-100) |
| idade | int | Idade do solicitante |
| num_dependentes | int | Número de dependentes |

**Target:** `inadimplente` (0 = negativo, 1 = positivo)

## Métricas (test set)

| Métrica | Valor |
|---------|-------|
| Accuracy | 0.680 |
| Precision (classe 1) | 0.451 |
| Recall (classe 1) | 0.264 |
| F1-score (classe 1) | 0.333 |

## Limitações

* Treinado com **dados sintéticos**, não reflete distribuições reais.
* RandomForest com hiperparâmetros padrão, sem tuning.
* Proporção de classes fixada na geração.
