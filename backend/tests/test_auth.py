from urllib.parse import parse_qs, urlparse

import jwt

from conftest import register


def test_registration_login_me_and_logout(client):
    registration = register(client)
    assert registration["user"]["email"] == "user@example.com"
    assert registration["user"]["role"] == "user"
    token = registration["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=headers).status_code == 200
    assert client.post("/api/auth/logout", headers=headers).status_code == 200
    login = client.post("/api/auth/login", json={"email": "USER@example.com", "password": "securepass123"})
    assert login.status_code == 200


def test_duplicate_email_and_bad_login(client):
    register(client)
    assert client.post("/api/auth/register", json={"email": "USER@example.com", "password": "anotherpass123"}).status_code == 409
    assert client.post("/api/auth/login", json={"email": "user@example.com", "password": "wrong"}).status_code == 401
    assert client.post("/api/auth/login", json={"email": "missing@example.com", "password": "wrong"}).status_code == 401


def test_password_validation(client):
    weak = client.post("/api/auth/register", json={"email": "user@example.com", "password": "onlyletters"})
    assert weak.status_code == 422


def test_missing_invalid_and_wrong_type_token(client, app):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401
    wrong_type = jwt.encode({"sub": "abc", "type": "reset", "exp": 4_000_000_000}, app.state.settings.secret_key, algorithm="HS256")
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {wrong_type}"}).status_code == 401


def test_password_reset_is_neutral_single_use_and_changes_password(client, app):
    register(client)
    response = client.post("/api/auth/password-reset/request", json={"email": "user@example.com"})
    missing = client.post("/api/auth/password-reset/request", json={"email": "missing@example.com"})
    assert response.status_code == missing.status_code == 200
    assert response.json() == missing.json()
    body = app.state.email_provider.outbox[-1]["body"]
    token = parse_qs(urlparse(body.split()[-1]).query)["token"][0]
    payload = {"token": token, "new_password": "newsecurepass456"}
    assert client.post("/api/auth/password-reset/confirm", json=payload).status_code == 200
    assert client.post("/api/auth/password-reset/confirm", json=payload).status_code == 400
    assert client.post("/api/auth/login", json={"email": "user@example.com", "password": "newsecurepass456"}).status_code == 200


def test_registration_uses_mock_email_and_history(client, auth, app):
    assert app.state.email_provider.name == "mock"
    assert len(app.state.email_provider.outbox) == 1
    history = client.get("/api/notifications/history", headers=auth).json()["items"]
    assert history[0]["kind"] == "registration"
    assert "body" not in history[0]

