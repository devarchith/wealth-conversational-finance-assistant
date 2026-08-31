from app.models import FinancialProfile, Recommendation, RecommendationSummary


def calculate_recommendations(profile: FinancialProfile) -> RecommendationSummary:
    income = profile.monthly_income
    expenses = profile.monthly_expenses
    surplus = round(income - expenses, 2)
    savings_rate = round(surplus / income, 4) if income > 0 else None
    expense_ratio = round(expenses / income, 4) if income > 0 else None
    target_months = {"conservative": 6, "moderate": 4, "aggressive": 3}[profile.risk_tolerance]
    emergency_target = round(expenses * target_months, 2)
    emergency_gap = round(max(0, emergency_target - profile.current_savings), 2)
    goal_progress = [
        {"id": goal.id, "name": goal.name, "progress": round(min(1, goal.current_amount / goal.target_amount), 4), "remaining": round(max(0, goal.target_amount - goal.current_amount), 2)}
        for goal in profile.goals
    ]
    recommendations: list[Recommendation] = []
    if income <= 0:
        recommendations.append(Recommendation(category="profile", priority="high", title="Complete income information", explanation="Add reliable monthly income before interpreting ratios or setting contribution targets."))
    elif surplus < 0:
        recommendations.append(Recommendation(category="spending", priority="high", title="Address the monthly deficit", explanation="Expenses exceed income. Review the largest adjustable categories and essential obligations before adding investment risk."))
    elif savings_rate is not None and savings_rate < 0.1:
        recommendations.append(Recommendation(category="savings", priority="medium", title="Create a sustainable savings margin", explanation="Your current surplus is below 10% of income. Treat 10% as a diagnostic reference, not a universal rule, and increase gradually if feasible."))
    else:
        recommendations.append(Recommendation(category="savings", priority="low", title="Protect your positive surplus", explanation="You have a positive monthly surplus. Automate an affordable portion and review it when income or essential costs change."))
    if emergency_gap > 0:
        recommendations.append(Recommendation(category="emergency_fund", priority="high" if surplus > 0 else "medium", title="Build liquid reserves", explanation=f"The educational target used here is {target_months} months of reported expenses. The estimated gap is {emergency_gap:.2f}; adjust for job stability, dependents, insurance, and available liquidity."))
    else:
        recommendations.append(Recommendation(category="emergency_fund", priority="low", title="Review reserve adequacy", explanation="Reported savings meet this simple emergency-fund heuristic. Confirm that the money is liquid and not already allocated to another goal."))
    if profile.monthly_investment > max(0, surplus):
        recommendations.append(Recommendation(category="risk", priority="high", title="Reconcile planned investing with cash flow", explanation="Planned monthly investing exceeds the reported surplus. Avoid funding investments by ignoring essential expenses or short-term obligations."))
    return RecommendationSummary(
        monthly_surplus=surplus,
        savings_rate=savings_rate,
        expense_ratio=expense_ratio,
        emergency_fund_target=emergency_target,
        emergency_fund_gap=emergency_gap,
        risk_profile=profile.risk_tolerance,
        goal_progress=goal_progress,
        recommendations=recommendations,
    )

