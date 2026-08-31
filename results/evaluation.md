# Chatbot Evaluation Results

Generated: 2026-08-31T21:47:48+00:00

> These are measured results from the repository's labeled test set. The AI comparison uses `MockAIProvider`, not an external foundation model.

## Summary

| Engine | Cases | Intent accuracy | Entity precision | Entity recall | Fallback rate |
|---|---:|---:|---:|---:|---:|
| rule_based | 15 | 100.0% | 100.0% | 95.0% | 13.3% |
| mock_ai | 15 | 100.0% | 100.0% | 100.0% | 13.3% |

## Method

Intent accuracy is exact-match accuracy. Entity precision and recall compare entity *types* rather than free-text spans. Fallback rate is the proportion classified as `fallback`; two cases are intentionally ambiguous/out of scope. Response relevance is not scored because no defensible objective label exists in this small reconstruction set.

## Case details

### rule_based

| Case | Category | Expected intent | Predicted intent | Correct |
|---|---|---|---|:---:|
| budget-1 | budgeting | budget_analysis | budget_analysis | yes |
| expense-1 | expenses | expense_analysis | expense_analysis | yes |
| save-1 | saving | savings_recommendation | savings_recommendation | yes |
| emergency-1 | saving | emergency_fund | emergency_fund | yes |
| risk-1 | risk | risk_assessment | risk_assessment | yes |
| diversify-1 | investment | diversification | diversification | yes |
| retire-1 | retirement | retirement | retirement | yes |
| funds-1 | investment | investment_education | investment_education | yes |
| stock-1 | investment | investment_education | investment_education | yes |
| goal-1 | goals | goal_planning | goal_planning | yes |
| negation-1 | negation | investment_education | investment_education | yes |
| multi-1 | multi_intent | retirement | retirement | yes |
| amount-1 | entity | savings_recommendation | savings_recommendation | yes |
| ambiguous-1 | ambiguity | fallback | fallback | yes |
| not-finance-1 | out_of_scope | fallback | fallback | yes |

### mock_ai

| Case | Category | Expected intent | Predicted intent | Correct |
|---|---|---|---|:---:|
| budget-1 | budgeting | budget_analysis | budget_analysis | yes |
| expense-1 | expenses | expense_analysis | expense_analysis | yes |
| save-1 | saving | savings_recommendation | savings_recommendation | yes |
| emergency-1 | saving | emergency_fund | emergency_fund | yes |
| risk-1 | risk | risk_assessment | risk_assessment | yes |
| diversify-1 | investment | diversification | diversification | yes |
| retire-1 | retirement | retirement | retirement | yes |
| funds-1 | investment | investment_education | investment_education | yes |
| stock-1 | investment | investment_education | investment_education | yes |
| goal-1 | goals | goal_planning | goal_planning | yes |
| negation-1 | negation | investment_education | investment_education | yes |
| multi-1 | multi_intent | retirement | retirement | yes |
| amount-1 | entity | savings_recommendation | savings_recommendation | yes |
| ambiguous-1 | ambiguity | fallback | fallback | yes |
| not-finance-1 | out_of_scope | fallback | fallback | yes |

## Limitations

The dataset is small and authored from report-derived domains. It does not establish real-world financial-advice quality, safety, fairness, or foundation-model performance. The mock AI provider is deterministic and exists to exercise intent/entity behavior without credentials.
