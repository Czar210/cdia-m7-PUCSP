from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import json
import os


def generate_all(n_samples: int = 1000,
                 n_features: int = 5,
                 n_informative: int = 3,
                 n_redundant: int = 1,
                 class_sep: float = 3.0,
                 weights=(0.7, 0.3),
                 random_state: int | None = 42,
                 outdir: str | Path | None = None,
                 domain: str | None = "credit"):
    """Generate a synthetic classification dataset and return a dict with DataFrame(s).

    Returns a dict: {"dataset": DataFrame}.
    If `outdir` is provided, this function will NOT write files; the caller can
    write them. (Writing is handled centrally in `ensure_data`).
    """
    # If domain is credit, delegate to credit generator
    if domain == "credit":
        # credit generator returns a dict of DataFrames
        return {"credit": generate_credit(n_samples=n_samples, seed=random_state)}

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        class_sep=class_sep,
        weights=list(weights),
        random_state=random_state,
    )

    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
    df["target"] = y

    return {"dataset": df}


def generate_credit(n_samples: int = 1000,
                    seed: int | None = 42,
                    proporcao_positivos: float = 0.3) -> tuple[pd.DataFrame, "np.ndarray", "np.ndarray"]:
    """Generate a synthetic credit dataset and return (df, X, y).

    Parameters
    - n_samples: number of rows to generate
    - seed: random seed
    - proporcao_positivos: desired overall proportion of positive cases (inadimplente).
      Must be between 0.05 and 0.95.

    Returns
    - (df, X, y): DataFrame with named features and target column `inadimplente`,
      `X` is a 2D numpy array of features (columns in the DataFrame excluding target),
      `y` is a 1D numpy array of target (0/1).

    Example
    ```python
    from Hug.generator import generate_credit
    df, X, y = generate_credit(n_samples=2000, seed=42, proporcao_positivos=0.25)
    ```
    """
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError("proporcao_positivos must be between 0.05 and 0.95")

    rng = np.random.default_rng(seed)

    # renda mensal: lognormal-like distribution
    renda_mensal = np.exp(rng.normal(np.log(3000), 0.6, size=n_samples)).round(2)
    # divida atual: fraction of renda, skewed
    divida_frac = np.clip(rng.normal(0.2, 0.15, size=n_samples), 0.0, 5.0)
    divida_atual = (renda_mensal * divida_frac).round(2)
    # historico_pagamentos: score 0-100
    historico_pagamentos = np.clip((rng.normal(75, 15, size=n_samples)), 0, 100).round(0).astype(int)
    # idade
    idade = rng.integers(18, 85, size=n_samples)
    # numero de dependentes
    num_dependentes = rng.integers(0, 6, size=n_samples)

    # base risk score
    with np.errstate(divide='ignore', invalid='ignore'):
        risk_factor = (divida_atual / (renda_mensal + 1)) * 2.0
    hist_factor = (100 - historico_pagamentos) / 100.0
    dep_factor = num_dependentes * 0.05
    prob = 0.05 + 0.6 * risk_factor + 0.3 * hist_factor + dep_factor * 0.02
    prob = np.clip(prob, 0.001, 0.999)

    # adjust probabilities to match desired overall proportion while preserving relative risk
    mean_raw = float(np.mean(prob))
    if mean_raw <= 0:
        adj_prob = prob
    else:
        scale = proporcao_positivos / mean_raw
        adj_prob = np.clip(prob * scale, 0.001, 0.999)

    inadimplente = rng.random(n_samples) < adj_prob

    df = pd.DataFrame({
        "renda_mensal": renda_mensal,
        "divida_atual": divida_atual,
        "historico_pagamentos": historico_pagamentos,
        "idade": idade,
        "num_dependentes": num_dependentes,
        "inadimplente": inadimplente.astype(int),
    })

    X = df[["renda_mensal", "divida_atual", "historico_pagamentos", "idade", "num_dependentes"]].to_numpy()
    y = df["inadimplente"].to_numpy()
    return df, X, y


def generate_churn(n_samples: int = 1000,
                   seed: int | None = 42,
                   proporcao_positivos: float = 0.3) -> tuple[pd.DataFrame, "np.ndarray", "np.ndarray"]:
    """Generate a simple churn dataset and return (df, X, y).

    Features: dias_sem_login, num_chamados, valor_mensalidade, meses_contrato, nps_score
    """
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError("proporcao_positivos must be between 0.05 and 0.95")
    rng = np.random.default_rng(seed)

    # initial churn signal
    churn = rng.choice([0, 1], size=n_samples, p=[1 - proporcao_positivos, proporcao_positivos])

    dias_sem_login = np.where(churn == 1, rng.integers(30, 180, n_samples), rng.integers(1, 30, n_samples))
    num_chamados = np.where(churn == 1, rng.integers(3, 15, n_samples), rng.integers(0, 4, n_samples))
    valor_mensalidade = rng.uniform(50, 500, n_samples).round(2)
    meses_contrato = np.where(churn == 1, rng.integers(1, 12, n_samples), rng.integers(6, 60, n_samples))
    nps_score = np.where(churn == 1, rng.integers(0, 6, n_samples), rng.integers(5, 11, n_samples))

    df = pd.DataFrame({
        "dias_sem_login": dias_sem_login,
        "num_chamados": num_chamados,
        "valor_mensalidade": valor_mensalidade,
        "meses_contrato": meses_contrato,
        "nps_score": nps_score,
        "churn": churn.astype(int),
    })

    X = df[["dias_sem_login", "num_chamados", "valor_mensalidade", "meses_contrato", "nps_score"]].to_numpy()
    y = df["churn"].to_numpy()
    return df, X, y


def generate_fraud(n_samples: int = 1000,
                   seed: int | None = 42,
                   proporcao_positivos: float = 0.02) -> tuple[pd.DataFrame, "np.ndarray", "np.ndarray"]:
    """Generate a simple fraud dataset and return (df, X, y).

    Features: amount, hour, num_items, customer_age, transaction_history_score
    Small positive rate by default (0.02).
    """
    if not (0.001 <= proporcao_positivos <= 0.5):
        raise ValueError("proporcao_positivos must be between 0.001 and 0.5 for fraud")
    rng = np.random.default_rng(seed)

    is_fraud = rng.choice([0, 1], size=n_samples, p=[1 - proporcao_positivos, proporcao_positivos])

    amount = np.where(is_fraud == 1, rng.uniform(200, 5000, n_samples), rng.uniform(1, 1000, n_samples)).round(2)
    hour = rng.integers(0, 24, size=n_samples)
    num_items = np.where(is_fraud == 1, rng.integers(1, 10, n_samples), rng.integers(1, 5, n_samples))
    customer_age = rng.integers(18, 80, size=n_samples)
    transaction_history_score = np.clip(rng.normal(60, 20, size=n_samples), 0, 100).round(0).astype(int)

    df = pd.DataFrame({
        "amount": amount,
        "hour": hour,
        "num_items": num_items,
        "customer_age": customer_age,
        "transaction_history_score": transaction_history_score,
        "is_fraud": is_fraud.astype(int),
    })

    X = df[["amount", "hour", "num_items", "customer_age", "transaction_history_score"]].to_numpy()
    y = df["is_fraud"].to_numpy()
    return df, X, y


def _write_outputs(data: dict, outdir: str | Path):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, value in data.items():
        if hasattr(value, "to_csv"):
            path = outdir / f"{name}.csv"
            value.to_csv(path, index=False)
            written.append(path)
    # create a simple metadata file listing datasets and columns
    info = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "files": [str(p.name) for p in written],
        "columns": {name: list(value.columns) for name, value in data.items() if hasattr(value, "columns")},
    }
    info_path = outdir / "generation_info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    return written, info_path


def generate_variations(class_seps=(1.0, 3.0, 0.5), **gen_kwargs):
    """Generate multiple datasets varying `class_sep`.

    Returns a dict mapping names to DataFrames, e.g. {"dataset_cs1_0": df, ...}.
    Additional keyword args are passed to `generate_all`.
    """
    results = {}
    for cs in class_seps:
        ds = generate_all(class_sep=cs, **gen_kwargs)
        # ds may be a dict of dataframes or a single dataframe
        if hasattr(ds, "to_csv"):
            key = f"dataset_cs{str(cs).replace('.', '_')}"
            results[key] = ds
        elif isinstance(ds, dict):
            for name, df in ds.items():
                key = f"{name}_cs{str(cs).replace('.', '_')}"
                results[key] = df
        else:
            # unexpected type: skip
            continue
    return results


if __name__ == "__main__":
    # convenience: write outputs when invoked directly
    out = os.environ.get("HUG_OUTPUT_DIR", "data")
    data = generate_all()
    written, info = _write_outputs(data, out)
    print("Wrote:")
    for p in written:
        print(" -", p)
    print("Metadata:", info)