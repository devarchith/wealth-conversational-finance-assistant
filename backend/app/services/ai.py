from abc import ABC, abstractmethod
import json
import re

import httpx

from app.models import Entity
from app.services.rule_engine import EngineResult, RESPONSES, detect_intents, extract_entities, preprocess


class AIProvider(ABC):
    name: str

    @abstractmethod
    def respond(self, message: str) -> EngineResult: ...


class MockAIProvider(AIProvider):
    """Deterministic intent+entity provider used without paid credentials."""

    name = "mock_ai"

    def respond(self, message: str) -> EngineResult:
        entities = extract_entities(message)
        intents = detect_intents(message, entities)
        normalized = preprocess(message)
        negated_types: set[str] = set()
        for entity in entities:
            if re.search(rf"\b(?:do not|don t|dont|avoid|without|no)\b.{{0,24}}\b{re.escape(entity.value)}\b", normalized):
                negated_types.add(entity.type)
        if negated_types:
            entities.append(Entity(type="negation", value=", ".join(sorted(negated_types))))

        if not intents:
            return EngineResult(RESPONSES["fallback"], "fallback", entities, 0.35)

        primary = intents[0]
        response_parts: list[str] = []
        if negated_types:
            response_parts.append(f"I understand that you want to avoid {', '.join(sorted(negated_types)).replace('_', ' ')}.")
            alternatives = "Focus on your goal, time horizon, liquidity, costs, and the risks of any alternative rather than substituting one product automatically."
            response_parts.append(alternatives)
        for intent in intents[:2]:
            response_parts.append(RESPONSES[intent])
        confidence = min(0.98, 0.74 + 0.05 * len(entities) + 0.04 * min(len(intents), 2))
        return EngineResult(" ".join(response_parts), primary, entities, round(confidence, 2))


class OpenAICompatibleProvider(AIProvider):
    name = "openai_compatible"

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def respond(self, message: str) -> EngineResult:
        system = (
            "You are a cautious financial-education intent and entity assistant. "
            "Never claim live market data, execute transactions, promise returns, or replace a licensed adviser. "
            "Return JSON with response, intent, entities (array of {type,value}), and confidence."
        )
        with httpx.Client(timeout=20) as client:
            result = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "temperature": 0, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": system}, {"role": "user", "content": message}]},
            )
            result.raise_for_status()
        payload = json.loads(result.json()["choices"][0]["message"]["content"])
        return EngineResult(
            response=str(payload["response"]),
            intent=str(payload["intent"]),
            entities=[Entity.model_validate(e) for e in payload.get("entities", [])],
            confidence=max(0.0, min(1.0, float(payload.get("confidence", 0.5)))),
        )

