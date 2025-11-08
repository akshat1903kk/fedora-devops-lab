import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from fastapi.testclient import TestClient


def test_status_endpoint():
    """Ensure /api/v1/status returns correct health data."""
    client = TestClient(app)
    response = client.get("/api/v1/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] in [
        "API is operational",
        "API is live",
    ]  # supports both versions
    assert "version" in data
