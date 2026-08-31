import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.store import MemoryStore


@pytest.fixture
def store():
    return MemoryStore()


@pytest.fixture
def app(store):
    settings = Settings(app_env="test", secret_key="test-secret-that-is-not-used-outside-tests", frontend_url="http://testserver")
    return create_app(settings=settings, store=store)


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


def register(client: TestClient, email: str = "user@example.com", password: str = "securepass123") -> dict:
    response = client.post("/api/auth/register", json={"email": email, "password": password})
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def auth(client):
    data = register(client)
    return {"Authorization": f"Bearer {data['access_token']}"}

