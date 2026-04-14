import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# ensure Fast-API and repo root are on sys.path
_fast_api_dir = str(Path(__file__).resolve().parent.parent)
_repo_root = str(Path(__file__).resolve().parent.parent.parent)
for p in [_fast_api_dir, _repo_root]:
    if p not in sys.path:
        sys.path.insert(0, p)

from main import app


@pytest.fixture
def client():
    """Fresh TestClient per test function."""
    return TestClient(app)
