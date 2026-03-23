from pathlib import Path
import os


def ensure_data(outdir: str | Path | None = None, n_customers: int | None = None, n_orders: int | None = None, seed=None, overwrite: bool = False):
    """Ensure synthetic data files exist in `outdir`.

    - Reads defaults from environment variables `HUG_OUTPUT_DIR`, `HUG_N_CUSTOMERS`, `HUG_N_ORDERS`, `HUG_SEED` when parameters are not provided.
    - If `customers.csv` or `orders.csv` is missing (or `overwrite=True`), calls `generator.generate_all()` and writes the CSVs.

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

    # Check for class_sep variations in env: comma-separated list
    class_seps_env = os.environ.get("HUG_CLASS_SEPS")
    class_seps = None
    if class_seps_env:
        try:
            class_seps = [float(s.strip()) for s in class_seps_env.split(",") if s.strip()]
        except ValueError:
            class_seps = None

    # Generate data: either variations or a single dataset
    if class_seps:
        data = generator.generate_variations(class_seps=class_seps)
        gen_params = {"class_seps": class_seps}
    else:
        try:
            data = generator.generate_all()
        except TypeError:
            try:
                data = generator.generate_all(random_state=seed)
            except Exception:
                data = generator.generate_all()
        gen_params = {}

    # Normalize and write each DataFrame to CSV
    import pandas as _pd

    if hasattr(data, "to_csv") or isinstance(data, _pd.DataFrame):
        data = {"dataset": data}

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
