from app.config import Settings
from app.main import build_providers
from app.security import hash_password
from conftest import register


def test_mock_storage_upload_and_validation(client, auth):
    result = client.post("/api/storage/upload", headers=auth, files={"file": ("avatar.png", b"not-a-real-image-but-test-content", "image/png")})
    assert result.status_code == 201
    assert result.json()["provider"] == "mock"
    assert result.json()["secure_url"].startswith("mock://")
    rejected = client.post("/api/storage/upload", headers=auth, files={"file": ("malware.exe", b"x", "application/octet-stream")})
    assert rejected.status_code == 415


def test_provider_fallback_when_credentials_missing():
    settings = Settings(app_env="test", ai_provider="openai", email_provider="smtp", storage_provider="cloudinary")
    ai, email, storage, fallbacks = build_providers(settings)
    assert (ai.name, email.name, storage.name) == ("mock_ai", "mock", "mock")
    assert set(fallbacks) == {"ai", "email", "storage"}


def test_admin_authorization_and_privacy_limited_summary(client, store):
    user = register(client)
    user_headers = {"Authorization": f"Bearer {user['access_token']}"}
    assert client.get("/api/admin/summary", headers=user_headers).status_code == 403
    admin = store.create_user("admin@example.com", hash_password("adminsecure123"), role="admin")
    login = client.post("/api/auth/login", json={"email": admin["email"], "password": "adminsecure123"}).json()
    result = client.get("/api/admin/summary", headers={"Authorization": f"Bearer {login['access_token']}"})
    assert result.status_code == 200
    assert result.json()["counts"]["users"] == 2
    assert "password" not in str(result.json()).lower()


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "available"


def test_production_rejects_insecure_runtime_modes():
    try:
        Settings(app_env="production", database_backend="memory", secret_key="a-real-deployment-secret")
    except ValueError as exc:
        assert "In-memory persistence" in str(exc)
    else:
        raise AssertionError("production accepted in-memory persistence")
