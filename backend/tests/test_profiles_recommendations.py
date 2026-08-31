from conftest import register


def test_profile_and_financial_profile_round_trip(client, auth):
    profile = {"display_name": "Dev", "preferred_currency": "usd", "timezone": "America/Los_Angeles", "financial_literacy": "intermediate", "avatar_url": None}
    saved = client.put("/api/profile", headers=auth, json=profile)
    assert saved.status_code == 200
    assert saved.json()["preferred_currency"] == "USD"
    assert client.get("/api/profile", headers=auth).json()["display_name"] == "Dev"

    financial = {"monthly_income": 5000, "monthly_expenses": 3200, "current_savings": 4000, "monthly_investment": 500, "risk_tolerance": "moderate", "investment_horizon_months": 84, "goals": [{"name": "Home deposit", "target_amount": 20000, "current_amount": 5000}]}
    saved_financial = client.put("/api/financial-profile", headers=auth, json=financial)
    assert saved_financial.status_code == 200
    assert saved_financial.json()["goals"][0]["id"]
    assert client.get("/api/financial-profile", headers=auth).json()["monthly_income"] == 5000


def test_recommendation_math_and_guardrails(client, auth):
    client.put("/api/financial-profile", headers=auth, json={"monthly_income": 4000, "monthly_expenses": 3000, "current_savings": 6000, "monthly_investment": 1500, "risk_tolerance": "moderate", "investment_horizon_months": 60, "goals": []})
    result = client.get("/api/recommendations", headers=auth)
    assert result.status_code == 200
    data = result.json()
    assert data["monthly_surplus"] == 1000
    assert data["savings_rate"] == 0.25
    assert data["expense_ratio"] == 0.75
    assert data["emergency_fund_target"] == 12000
    assert data["emergency_fund_gap"] == 6000
    assert any(r["title"] == "Reconcile planned investing with cash flow" for r in data["recommendations"])


def test_profiles_are_user_isolated(client):
    first = register(client, "first@example.com")
    second = register(client, "second@example.com")
    h1 = {"Authorization": f"Bearer {first['access_token']}"}
    h2 = {"Authorization": f"Bearer {second['access_token']}"}
    client.put("/api/profile", headers=h1, json={"display_name": "First"})
    assert client.get("/api/profile", headers=h2).json()["display_name"] == ""

