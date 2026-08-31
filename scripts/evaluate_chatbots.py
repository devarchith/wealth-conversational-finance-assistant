#!/usr/bin/env python3
"""Evaluate both reconstructed chatbot designs against labeled finance queries."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.services.ai import MockAIProvider  # noqa: E402
from app.services.rule_engine import RuleBasedEngine  # noqa: E402


def safe_ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 1.0


def evaluate(engine, cases: list[dict]) -> dict:
    rows: list[dict] = []
    intent_hits = entity_hits = expected_entity_total = predicted_entity_total = fallbacks = 0
    for case in cases:
        result = engine.respond(case["query"])
        predicted = {entity.type for entity in result.entities}
        expected = set(case["expected_entities"])
        correct_entities = predicted & expected
        intent_correct = result.intent == case["expected_intent"]
        intent_hits += int(intent_correct)
        entity_hits += len(correct_entities)
        expected_entity_total += len(expected)
        predicted_entity_total += len(predicted)
        fallbacks += int(result.intent == "fallback")
        rows.append({
            "id": case["id"], "category": case["category"], "query": case["query"],
            "expected_intent": case["expected_intent"], "predicted_intent": result.intent,
            "intent_correct": intent_correct, "expected_entities": sorted(expected),
            "predicted_entities": sorted(predicted), "confidence": result.confidence,
        })
    return {
        "engine": engine.name,
        "metrics": {
            "cases": len(cases),
            "intent_accuracy": safe_ratio(intent_hits, len(cases)),
            "entity_precision": safe_ratio(entity_hits, predicted_entity_total),
            "entity_recall": safe_ratio(entity_hits, expected_entity_total),
            "fallback_rate": safe_ratio(fallbacks, len(cases)),
        },
        "cases": rows,
    }


def markdown_report(payload: dict) -> str:
    lines = [
        "# Chatbot Evaluation Results", "",
        f"Generated: {payload['generated_at']}", "",
        "> These are measured results from the repository's labeled test set. The AI comparison uses `MockAIProvider`, not an external foundation model.", "",
        "## Summary", "",
        "| Engine | Cases | Intent accuracy | Entity precision | Entity recall | Fallback rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for result in payload["results"]:
        metrics = result["metrics"]
        lines.append(f"| {result['engine']} | {metrics['cases']} | {metrics['intent_accuracy']:.1%} | {metrics['entity_precision']:.1%} | {metrics['entity_recall']:.1%} | {metrics['fallback_rate']:.1%} |")
    lines += ["", "## Method", "", "Intent accuracy is exact-match accuracy. Entity precision and recall compare entity *types* rather than free-text spans. Fallback rate is the proportion classified as `fallback`; two cases are intentionally ambiguous/out of scope. Response relevance is not scored because no defensible objective label exists in this small reconstruction set.", "", "## Case details", ""]
    for result in payload["results"]:
        lines += [f"### {result['engine']}", "", "| Case | Category | Expected intent | Predicted intent | Correct |", "|---|---|---|---|:---:|"]
        for row in result["cases"]:
            lines.append(f"| {row['id']} | {row['category']} | {row['expected_intent']} | {row['predicted_intent']} | {'yes' if row['intent_correct'] else 'no'} |")
        lines.append("")
    lines += ["## Limitations", "", "The dataset is small and authored from report-derived domains. It does not establish real-world financial-advice quality, safety, fairness, or foundation-model performance. The mock AI provider is deterministic and exists to exercise intent/entity behavior without credentials.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=ROOT / "evaluation" / "test_queries.json")
    parser.add_argument("--results", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text())
    payload = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "provider_note": "AI results use MockAIProvider; no external AI API was called.",
        "results": [evaluate(RuleBasedEngine(), cases), evaluate(MockAIProvider(), cases)],
    }
    args.results.mkdir(parents=True, exist_ok=True)
    (args.results / "evaluation.json").write_text(json.dumps(payload, indent=2) + "\n")
    (args.results / "evaluation.md").write_text(markdown_report(payload))
    print(json.dumps({r["engine"]: r["metrics"] for r in payload["results"]}, indent=2))


if __name__ == "__main__":
    main()

