import os
import joblib
from huggingface_hub import hf_hub_download


def load_model(
    repo_id: str | None = None,
    filename: str = "model.pkl",
    force_download: bool = False,
):
    """Download (or load from cache) a model from the Hugging Face Hub.

    Falls back to the local MODEL_PATH env var if repo_id is not provided.
    """
    if repo_id is None:
        local_path = os.environ.get("MODEL_PATH", "model.pkl")
        if os.path.isfile(local_path):
            return joblib.load(local_path)
        raise FileNotFoundError(
            f"No repo_id provided and local model not found at {local_path}"
        )

    token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    local_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        force_download=force_download,
        token=token,
    )
    return joblib.load(local_path)
