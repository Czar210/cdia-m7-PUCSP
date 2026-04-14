"""Upload trained model artifacts to the Hugging Face Hub.

Usage:
    python -m Hug.upload_to_hub          # uses defaults
    python -m Hug.upload_to_hub --domain credit --repo-id user/my-model
"""
import os
import argparse
from pathlib import Path

from dotenv import load_dotenv

# load .env from repo root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import sklearn
import joblib as jl
import numpy as np
from huggingface_hub import HfApi, login


def build_model_card(domain: str, repo_id: str, metrics_path: Path) -> str:
    import json

    metrics = {}
    if metrics_path.exists():
        with open(metrics_path, encoding="utf-8") as f:
            metrics = json.load(f)

    acc = metrics.get("accuracy", "N/A")
    pos = metrics.get("1", {})
    precision = pos.get("precision", "N/A")
    recall = pos.get("recall", "N/A")
    f1 = pos.get("f1-score", "N/A")

    feature_tables = {
        "credit": """| Feature | Tipo | Descrição |
|---------|------|-----------|
| renda_mensal | float | Renda mensal em reais |
| divida_atual | float | Dívida atual em reais |
| historico_pagamentos | int | Score de histórico (0-100) |
| idade | int | Idade do solicitante |
| num_dependentes | int | Número de dependentes |""",
        "churn": """| Feature | Tipo | Descrição |
|---------|------|-----------|
| dias_sem_login | int | Dias desde o último login |
| num_chamados | int | Número de chamados abertos |
| valor_mensalidade | float | Valor da mensalidade |
| meses_contrato | int | Meses de contrato |
| nps_score | int | Score NPS (0-10) |""",
        "fraud": """| Feature | Tipo | Descrição |
|---------|------|-----------|
| amount | float | Valor da transação |
| hour | int | Hora da transação (0-23) |
| num_items | int | Número de itens |
| customer_age | int | Idade do cliente |
| transaction_history_score | int | Score de histórico (0-100) |""",
    }

    target_names = {"credit": "inadimplente", "churn": "churn", "fraud": "is_fraud"}
    features_md = feature_tables.get(domain, "Consulte o código para lista de features.")
    target = target_names.get(domain, "target")

    return f"""---
language: pt
tags:
  - sklearn
  - classification
  - {domain}
  - mlops
---

# {repo_id.split('/')[-1]}

Modelo RandomForest para classificação binária — domínio **{domain}**.
Desenvolvido como parte do curso CDIA M7 — Semana 3.

## Uso

```python
from huggingface_hub import hf_hub_download
import joblib

model = joblib.load(hf_hub_download("{repo_id}", "model.pkl"))
prediction = model.predict([[...]])
```

## Features de entrada

{features_md}

**Target:** `{target}` (0 = negativo, 1 = positivo)

## Métricas (test set)

| Métrica | Valor |
|---------|-------|
| Accuracy | {acc if isinstance(acc, str) else f'{acc:.3f}'} |
| Precision (classe 1) | {precision if isinstance(precision, str) else f'{precision:.3f}'} |
| Recall (classe 1) | {recall if isinstance(recall, str) else f'{recall:.3f}'} |
| F1-score (classe 1) | {f1 if isinstance(f1, str) else f'{f1:.3f}'} |

## Limitações

- Treinado com **dados sintéticos** — não reflete distribuições reais.
- RandomForest com hiperparâmetros padrão, sem tuning.
- Proporção de classes fixada na geração.
"""


def upload(domain: str = "credit", repo_id: str | None = None):
    token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("Set HUGGINGFACE_HUB_TOKEN or HF_TOKEN env var")

    login(token=token)
    api = HfApi()

    if repo_id is None:
        username = api.whoami()["name"]
        repo_id = f"{username}/mlops-{domain}-v1"

    api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True, private=False)
    print(f"Repositório: https://huggingface.co/{repo_id}")

    models_dir = Path(__file__).resolve().parent / "data" / "models"
    model_path = models_dir / f"{domain}_rf.pkl"
    metrics_path = models_dir / f"{domain}_metrics.json"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run train_and_save.py first."
        )

    # model card
    card = build_model_card(domain, repo_id, metrics_path)
    card_path = models_dir / f"{domain}_README.md"
    card_path.write_text(card, encoding="utf-8")

    # requirements
    reqs = f"scikit-learn=={sklearn.__version__}\njoblib=={jl.__version__}\nnumpy=={np.__version__}\n"
    reqs_path = models_dir / f"{domain}_requirements.txt"
    reqs_path.write_text(reqs, encoding="utf-8")

    uploads = [
        (model_path, "model.pkl"),
        (card_path, "README.md"),
        (reqs_path, "requirements.txt"),
    ]
    if metrics_path.exists():
        uploads.append((metrics_path, "metrics.json"))

    for local, remote in uploads:
        api.upload_file(
            path_or_fileobj=str(local),
            path_in_repo=remote,
            repo_id=repo_id,
            repo_type="model",
            commit_message=f"Add {remote}",
        )
        print(f"  {remote} uploaded")

    print(f"\nDone: https://huggingface.co/{repo_id}")
    return repo_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload model to HF Hub")
    parser.add_argument("--domain", default="credit", choices=["credit", "churn", "fraud"])
    parser.add_argument("--repo-id", default=None, help="e.g. username/mlops-credit-v1")
    args = parser.parse_args()
    upload(domain=args.domain, repo_id=args.repo_id)
