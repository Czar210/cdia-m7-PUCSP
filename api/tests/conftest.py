import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

_api_dir = str(Path(__file__).resolve().parent.parent)
if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

from main import app


@pytest.fixture
def client():
    """Fresh TestClient per test function."""
    return TestClient(app)
