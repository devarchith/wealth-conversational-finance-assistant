import re
from dataclasses import dataclass

from app.models import Entity


ENTITY_TERMS: dict[str, tuple[str, ...]] = {
    "budget": ("budget", "budgeting", "spending plan"),
    "savings": ("save", "saving", "savings"),
    "emergency_fund": ("emergency fund", "rainy day fund"),
    "stocks": ("stock", "stocks", "equity", "equities", "shares"),
    "mutual_funds": ("mutual fund", "mutual funds", "index fund", "index funds"),
    "retirement": ("retirement", "retire", "401k", "401(k)", "ira"),
    "risk": ("risk", "volatility", "loss"),
    "diversification": ("diversify", "diversification", "diversified"),
    "expenses": ("expense", "expenses", "spending", "costs"),
    "goals": ("goal", "goals", "target"),
    "investing": ("invest", "investing", "investment", "portfolio"),
}

INTENT_PRIORITY = [
    "emergency_fund", "retirement", "diversification", "risk_assessment",
    "budget_analysis", "expense_analysis", "savings_recommendation",
    "goal_planning", "investment_education",
]

RESPONSES = {
    "budget_analysis": "Start by comparing monthly income with essential, flexible, and discretionary expenses. Use the dashboard surplus and expense-ratio metrics to identify a realistic adjustment; do not cut essentials to satisfy a generic rule.",
    "expense_analysis": "Review recurring and discretionary expenses separately, then investigate the largest changeable categories. A useful first step is to compare each category with your monthly income rather than treating every expense equally.",
    "savings_recommendation": "Automate a sustainable amount after essential bills and build consistency before increasing it. Your financial profile can estimate a savings rate, but the right target depends on income stability and near-term obligations.",
    "emergency_fund": "An emergency fund is cash reserved for unplanned essential costs. A common educational range is three to six months of essential expenses, adjusted for job stability, dependents, insurance, and access to other liquidity.",
    "retirement": "Retirement planning usually combines time horizon, contribution consistency, tax-advantaged accounts available in your country, costs, and diversification. Verify account and tax rules with an authoritative local source.",
    "risk_assessment": "Risk capacity depends on time horizon, income stability, liquidity needs, and ability to tolerate losses. Risk tolerance is psychological; risk capacity is financial, and the more conservative of the two should constrain a plan.",
    "diversification": "Diversification spreads exposure across assets, sectors, and regions, reducing dependence on a single outcome. It does not prevent losses, and overlapping funds may be less diversified than they appear.",
    "goal_planning": "Define a target amount and date, subtract current dedicated savings, then calculate a feasible monthly contribution. Prioritize essential resilience before optional goals and revisit assumptions when income or costs change.",
    "investment_education": "Before choosing an investment, clarify the goal, time horizon, liquidity needs, risk capacity, fees, diversification, and taxes. This assistant does not rank live securities or promise returns.",
    "fallback": "I can help with budgeting, savings, emergency funds, expenses, investing basics, diversification, risk, financial goals, retirement, stocks, and mutual funds. Try asking one specific finance question.",
}


@dataclass
class EngineResult:
    response: str
    intent: str
    entities: list[Entity]
    confidence: float


def preprocess(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9%()$ ]", " ", text.lower())).strip()


def extract_entities(text: str) -> list[Entity]:
    normalized = preprocess(text)
    entities: list[Entity] = []
    for entity_type, terms in ENTITY_TERMS.items():
        matched = next((term for term in terms if re.search(rf"\b{re.escape(term)}\b", normalized)), None)
        if matched:
            entities.append(Entity(type=entity_type, value=matched))
    amounts = re.findall(r"(?:\$\s*)?\b\d+(?:\.\d+)?\s*%?", text)
    entities.extend(Entity(type="amount", value=value.strip()) for value in amounts[:5])
    return entities


def detect_intents(text: str, entities: list[Entity]) -> list[str]:
    normalized = preprocess(text)
    found: set[str] = set()
    entity_types = {e.type for e in entities}
    if "emergency_fund" in entity_types:
        found.add("emergency_fund")
    if "retirement" in entity_types:
        found.add("retirement")
    if "diversification" in entity_types:
        found.add("diversification")
    if "risk" in entity_types:
        found.add("risk_assessment")
    if "budget" in entity_types or any(x in normalized for x in ("afford", "surplus")):
        found.add("budget_analysis")
    if "expenses" in entity_types:
        found.add("expense_analysis")
    if "savings" in entity_types:
        found.add("savings_recommendation")
    if "goals" in entity_types:
        found.add("goal_planning")
    if entity_types & {"stocks", "mutual_funds", "investing"}:
        found.add("investment_education")
    return [intent for intent in INTENT_PRIORITY if intent in found]


class RuleBasedEngine:
    name = "rule_based"

    def respond(self, message: str) -> EngineResult:
        entities = extract_entities(message)
        intents = detect_intents(message, entities)
        if not intents:
            return EngineResult(RESPONSES["fallback"], "fallback", entities, 0.2)
        primary = intents[0]
        confidence = min(0.94, 0.55 + 0.1 * len(entities) + (0.08 if len(intents) == 1 else 0))
        return EngineResult(RESPONSES[primary], primary, entities, round(confidence, 2))

