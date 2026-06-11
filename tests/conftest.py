import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def admin_token():
    response = client.post(
        "/auth/token",
        data={
            "username": "pt",
            "password": "1234"
        }
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def student_token():
    response = client.post(
        "/auth/token",
        data={
            "username": "j",
            "password": "1234"
        }
    )

    assert response.status_code == 200
    return response.json()["access_token"]