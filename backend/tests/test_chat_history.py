from conftest import register


def test_rule_chat_intent_entities_and_history(client, auth):
    response = client.post("/api/chat/rule-based", headers=auth, json={"message": "How should I build an emergency fund?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "emergency_fund"
    assert data["engine"] == "rule_based"
    assert any(e["type"] == "emergency_fund" for e in data["entities"])
    history = client.get("/api/history", headers=auth).json()
    assert history["total"] == 1
    detail = client.get(f"/api/history/{data['conversation_id']}", headers=auth).json()
    assert [m["role"] for m in detail["messages"]] == ["user", "assistant"]


def test_ai_mock_handles_negation_and_multi_intent(client, auth):
    response = client.post("/api/chat/ai", headers=auth, json={"message": "I don't want stocks; how can I save and diversify?"})
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "mock_ai"
    assert any(e["type"] == "negation" for e in data["entities"])
    assert "avoid" in data["response"].lower()


def test_fallback_and_continue_conversation(client, auth):
    first = client.post("/api/chat/rule-based", headers=auth, json={"message": "hello there"}).json()
    assert first["intent"] == "fallback"
    second = client.post("/api/chat/rule-based", headers=auth, json={"message": "Explain mutual funds", "conversation_id": first["conversation_id"]})
    assert second.status_code == 200
    detail = client.get(f"/api/history/{first['conversation_id']}", headers=auth).json()
    assert len(detail["messages"]) == 4


def test_history_strict_user_isolation_and_delete(client):
    one = register(client, "one@example.com")
    two = register(client, "two@example.com")
    h1 = {"Authorization": f"Bearer {one['access_token']}"}
    h2 = {"Authorization": f"Bearer {two['access_token']}"}
    conversation_id = client.post("/api/chat/ai", headers=h1, json={"message": "Help with my budget"}).json()["conversation_id"]
    assert client.get(f"/api/history/{conversation_id}", headers=h2).status_code == 404
    assert client.delete(f"/api/history/{conversation_id}", headers=h2).status_code == 404
    assert client.delete(f"/api/history/{conversation_id}", headers=h1).status_code == 204
    assert client.get(f"/api/history/{conversation_id}", headers=h1).status_code == 404


def test_rejects_foreign_conversation_on_chat(client):
    one = register(client, "a@example.com")
    two = register(client, "b@example.com")
    h1 = {"Authorization": f"Bearer {one['access_token']}"}
    h2 = {"Authorization": f"Bearer {two['access_token']}"}
    conversation_id = client.post("/api/chat/rule-based", headers=h1, json={"message": "budget"}).json()["conversation_id"]
    response = client.post("/api/chat/ai", headers=h2, json={"message": "save", "conversation_id": conversation_id})
    assert response.status_code == 404

