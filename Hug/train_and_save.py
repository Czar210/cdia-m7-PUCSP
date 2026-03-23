from pathlib import Path
import json
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_recall_fscore_support

from . import generator


def train_on_domain(domain: str, n_samples: int = 2000, seed: int = 42, proporcao_positivos: float | None = None):
    """Generate dataset for `domain`, train RandomForest, save model and metrics.

    Returns dict with paths and brief interpretation for positive class.
    """
    out_base = Path("Hug") / "data" / "models"
    out_base.mkdir(parents=True, exist_ok=True)

    # select generator
    if domain == "credit":
        df, X, y = generator.generate_credit(n_samples=n_samples, seed=seed, proporcao_positivos=(proporcao_positivos or 0.3))
    elif domain == "churn":
        df, X, y = generator.generate_churn(n_samples=n_samples, seed=seed, proporcao_positivos=(proporcao_positivos or 0.3))
    elif domain == "fraud":
        df, X, y = generator.generate_fraud(n_samples=n_samples, seed=seed, proporcao_positivos=(proporcao_positivos if proporcao_positivos is not None else 0.02))
    else:
        raise ValueError("unknown domain")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=seed)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    report_text = classification_report(y_test, y_pred)
    print(f"=== Domain: {domain} ===")
    print(report_text)

    # positive class metrics
    pos_label = "1"
    if "1" in report:
        pos = report["1"]
        precision = pos.get("precision", 0.0)
        recall = pos.get("recall", 0.0)
        f1 = pos.get("f1-score", 0.0)
    else:
        # fallback
        p, r, f1, _ = precision_recall_fscore_support(y_test, y_pred, average=None, zero_division=0)
        # find index for positive label
        try:
            idx = list(set(y_test)).index(1)
            precision, recall, f1 = p[idx], r[idx], f1[idx]
        except Exception:
            precision = recall = f1 = 0.0

    interp = f"Positive class metrics — precision: {precision:.2f}, recall: {recall:.2f}, f1: {f1:.2f}"
    print(interp)

    # save model and metrics
    model_path = out_base / f"{domain}_rf.pkl"
    metrics_path = out_base / f"{domain}_metrics.json"
    txt_report_path = out_base / f"{domain}_classification_report.txt"

    joblib.dump(model, model_path)

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    with open(txt_report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
        f.write("\n\n")
        f.write(interp)

    return {"model": str(model_path), "metrics": str(metrics_path), "report": str(txt_report_path), "interpretation": interp}


if __name__ == "__main__":
    domains = ["credit", "churn", "fraud"]
    results = {}
    for d in domains:
        try:
            results[d] = train_on_domain(d)
        except Exception as e:
            results[d] = {"error": str(e)}
    print("Done. Artifacts:")
    print(json.dumps(results, indent=2))
