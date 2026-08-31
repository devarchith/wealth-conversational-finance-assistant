#!/usr/bin/env python3
"""Exercise the running backend through its public HTTP contract."""

from __future__ import annotations

import argparse
import time

import httpx


def require(response: httpx.Response, status: int) -> dict:
    if response.status_code != status:
        raise RuntimeError(f"{response.request.method} {response.request.url.path}: expected {status}, got {response.status_code}: {response.text}")
    return response.json() if response.content else {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/api")
    args = parser.parse_args()
    email = f"smoke-{int(time.time())}@example.com"
    password = "integrationpass123"
    with httpx.Client(base_url=args.base_url, timeout=10, trust_env=False) as client:
        health = require(client.get("/health"), 200)
        registration = require(client.post("/auth/register", json={"email": email, "password": password}), 201)
        headers = {"Authorization": f"Bearer {registration['access_token']}"}
        require(client.post("/auth/login", json={"email": email, "password": password}), 200)
        require(client.get("/auth/me", headers=headers), 200)
        require(client.put("/profile", headers=headers, json={"display_name": "Smoke Test", "preferred_currency": "USD", "financial_literacy": "beginner", "timezone": "UTC"}), 200)
        require(client.put("/financial-profile", headers=headers, json={"monthly_income": 5000, "monthly_expenses": 3400, "current_savings": 5000, "monthly_investment": 400, "risk_tolerance": "moderate", "investment_horizon_months": 84, "goals": [{"name": "Emergency reserve", "target_amount": 13600, "current_amount": 5000}]}), 200)
        metrics = require(client.get("/recommendations", headers=headers), 200)
        if metrics["monthly_surplus"] != 1600:
            raise RuntimeError("Recommendation arithmetic mismatch")
        rule = require(client.post("/chat/rule-based", headers=headers, json={"message": "How should I build an emergency fund?"}), 200)
        ai = require(client.post("/chat/ai", headers=headers, json={"message": "I do not want stocks; how can I diversify?", "conversation_id": rule["conversation_id"]}), 200)
        if ai["engine"] != "mock_ai":
            raise RuntimeError("Expected credential-free mock AI provider")
        history = require(client.get("/history", headers=headers), 200)
        require(client.get(f"/history/{rule['conversation_id']}", headers=headers), 200)
        require(client.post("/storage/upload", headers=headers, files={"file": ("profile.png", b"smoke", "image/png")}), 201)
        notifications = require(client.get("/notifications/history", headers=headers), 200)
        require(client.post("/auth/logout", headers=headers), 200)
        print({"health": health["status"], "database": health["database"], "surplus": metrics["monthly_surplus"], "conversations": history["total"], "notifications": len(notifications["items"]), "engines": [rule["engine"], ai["engine"]]})


if __name__ == "__main__":
    main()
