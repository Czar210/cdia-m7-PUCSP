from pathlib import Path
import os


def ensure_data(outdir: str | Path | None = None, seed=None, overwrite: bool = False):
    """Ensure synthetic data files exist in `outdir`.

    - Reads defaults from environment variables `HUG_OUTPUT_DIR` and `HUG_SEED`.
    - If no CSVs exist (or `overwrite=True`), generates credit, churn, and fraud datasets.

    Returns a dict with paths and a `generated` boolean.
    """
    outdir = Path(outdir or os.environ.get("HUG_OUTPUT_DIR", "./data"))
    outdir.mkdir(parents=True, exist_ok=True)

    # if any CSVs already exist in outdir and not overwrite, skip generation
    existing_csvs = list(outdir.glob("*.csv"))
    if existing_csvs and not overwrite:
        return {"files": existing_csvs, "generated": False}

    # Resolve simple generation params (seed only); generator may ignore extras
    env_seed = os.environ.get("HUG_SEED")
    if seed is None and env_seed is not None and env_seed != "":
        try:
            seed = int(env_seed)
        except ValueError:
            seed = env_seed

    # Lazy import to keep module lightweight
    from . import generator

    # Generate all three domains
    seed_val = seed if seed is not None else 42

    credit_df, _, _ = generator.generate_credit(n_samples=1000, seed=seed_val)
    churn_df, _, _ = generator.generate_churn(n_samples=1000, seed=seed_val)
    fraud_df, _, _ = generator.generate_fraud(n_samples=1000, seed=seed_val)

    data = {"credit": credit_df, "churn": churn_df, "fraud": fraud_df}
    gen_params = {"seed": seed_val, "n_samples": 1000}

    written = []
    for name, val in data.items():
        if hasattr(val, "to_csv"):
            path = outdir / f"{name}.csv"
            val.to_csv(path, index=False)
            written.append(path)

    # metadata file with names of infos used to generate (column names + params)
    info = {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "files": [p.name for p in written],
        "columns": {name: list(val.columns) for name, val in data.items() if hasattr(val, "columns")},
        "params": gen_params,
    }
    info_path = outdir / "generation_info.json"
    import json

    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

    return {"files": written, "info": info_path, "generated": True}
