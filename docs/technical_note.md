# Technical Note

## Responsible Customer Lifetime Value / Next-Best-Action Model

This technical note summarises the analytical design behind the Credit Growth Analytics Pipeline. The repository uses synthetic financial-services data to demonstrate how a customer-growth problem can be translated into a governed decision-ranking system.

The core objective is to prioritise customers for credit-growth actions by combining:

```text
P(conversion) × P(responsible credit behaviour) × Expected Credit Value
```

The project is designed for finance, customer analytics, credit risk analytics, BI, and commercial data science use cases.

---

## 1. Business Problem

Financial institutions need to grow credit portfolios without encouraging unsuitable lending or relying only on broad manual segmentation. A traditional campaign may select customers using static rules such as income, tenure, age group, or current product ownership. That approach can be useful, but it does not explicitly balance conversion likelihood, responsible behaviour, and commercial value.

This project reframes the problem as a Next-Best-Action ranking question:

> Which customer should receive which suitable credit action, based on conversion likelihood, expected responsible behaviour, expected value, and governance filters?

The model is not intended to automate credit approval. It supports prioritisation, campaign targeting, and decision intelligence.

---

## 2. Data Design

The repository uses synthetic data only. No real customer or institutional data is included.

The synthetic data simulates a customer-month analytical base with the following domains:

| Domain | Example fields | Purpose |
|---|---|---|
| Customer profile | age, income band, region, employment type, tenure | baseline customer segmentation |
| Behavioural signals | savings balance, credit balance, engagement, balance growth | recent customer behaviour |
| Credit risk proxy | utilisation ratio, arrears signal, affordability proxy | responsible-lending guardrails |
| Product catalogue | loan amount, margin, cost, expected loss | expected value calculation |
| Outcomes | conversion in 3 months, responsible behaviour in 6 months | supervised targets |
| Treatment log sample | recommended action, contacted flag, outcome window | future intervention learning |

The current synthetic configuration creates 1,200 customers over 18 monthly snapshots, producing 21,600 customer-month observations before temporal splitting.

---

## 3. Feature Engineering

The modelling layer uses a governed feature list with numeric and categorical variables.

Representative features include:

| Feature group | Examples |
|---|---|
| Profile | age, tenure, annual income, income band score |
| Engagement | digital engagement score, engagement score, salary inflow flag |
| Financial behaviour | savings balance, credit balance, recent balance growth |
| Credit exposure | utilisation ratio, credit-to-income ratio, arrears in last 6 months |
| Relationship depth | number of products, product depth score |
| Affordability | affordability proxy, balance-to-income ratio |
| Categorical context | region, employment type, customer segment |

The project separates feature construction from model training, scoring, validation, and governance so that the pipeline remains reproducible and auditable.

---

## 4. Modelling Approach

The analytical design uses two supervised classification models and one value calculation layer.

| Component | Target / output | Role in final score |
|---|---|---|
| Conversion model | `converted_next_3m` | estimates `p_conversion` |
| Responsible behaviour model | `responsible_credit_behaviour_6m` | estimates `p_responsible` |
| Expected value layer | product-level expected value | estimates commercial value by recommended product |

The current implemented classifier is an `ExtraTreesClassifier` wrapped inside a scikit-learn `Pipeline` with numeric imputation and categorical one-hot encoding. The model uses 120 estimators, maximum depth 9, minimum leaf size 25, balanced class weights, fixed random seed, and parallel training.

A full model specification is available in [`docs/ml_model_specification.md`](ml_model_specification.md).

The final ranking score is:

```text
responsible_nba_score = p_conversion × p_responsible × expected_credit_value × eligibility_flag
```

The eligibility flag sets the score to zero when a customer fails responsible-lending guardrails.

---

## 5. Responsible-Lending and Eligibility Logic

Before ranking customers for action, the pipeline applies simple governance filters:

| Rule | Exclusion logic |
|---|---|
| Recent arrears | exclude if arrears signal is present |
| High utilisation | exclude if utilisation ratio is above 90% |
| No stable income signal | exclude if salary inflow flag is not present |
| Low income threshold | exclude if annual income is below the portfolio threshold |

These are simplified synthetic rules. In a real institution, they would need to be replaced by formal affordability, risk, compliance, consent, and fair-treatment controls.

---

## 6. Validation Strategy

The validation design compares three approaches:

| Approach | Description |
|---|---|
| Manual rule-based segmentation | transparent rule score using income, engagement, salary signal, arrears, and utilisation |
| Conversion-only model | ranks customers only by estimated conversion probability |
| Responsible NBA model | ranks customers by conversion probability, responsible behaviour probability, expected value, and eligibility |

Current synthetic benchmark:

| Approach | Precision@50 conversion | Precision@50 responsible conversion | Expected value captured | Eligible share |
|---|---:|---:|---:|---:|
| Manual rule-based segmentation | 20% | 16% | £59,500 | 100% |
| Conversion-only model | 26% | 20% | £55,196 | 82% |
| Responsible NBA model | 24% | 22% | £59,500 | 100% |

Interpretation: in this synthetic run, the conversion-only model produces the highest raw conversion Precision@50, but the Responsible NBA model produces the strongest responsible-conversion Precision@50 while preserving expected value capture and full eligible-share discipline.

---

## 7. Model Performance

Current synthetic model metrics:

| Model | Target | ROC-AUC | PR-AUC | Brier score | Precision@50 | Precision@100 |
|---|---|---:|---:|---:|---:|---:|
| Conversion model | `converted_next_3m` | 0.631 | 0.155 | 0.225 | 28% | 27% |
| Responsible behaviour model | `responsible_credit_behaviour_6m` | 0.649 | 0.868 | 0.230 | 92% | 90% |

The metrics should be read as synthetic demonstration results, not as evidence of performance on a real financial-services portfolio.

---

## 8. Output Layer

The pipeline produces dashboard-ready outputs for technical and non-technical review:

| Output | Purpose |
|---|---|
| `dashboard/data/model_metrics.csv` | model KPIs |
| `dashboard/data/benchmark_comparison.csv` | benchmark comparison across targeting approaches |
| `dashboard/data/nba_ranked_customers.csv` | customer-level Next-Best-Action ranking |
| `dashboard/data/governance_checks.csv` | audit and governance checks |
| `dashboard/data/segment_summary.csv` | segment-level business interpretation |

The visualisation layer is implemented in Streamlit as a public equivalent of a Power BI dashboard.

---

## 9. Governance and Limitations

The governance layer covers:

- time-ordered train/test splitting;
- duplicate key checks;
- missingness checks;
- leakage-oriented validation tests;
- responsible-lending exclusions;
- model-card documentation;
- dashboard-ready governance monitoring;
- treatment-log structure for future learning.

Key limitations:

1. the data is synthetic;
2. the value model is simplified;
3. eligibility rules are illustrative;
4. the model does not automate approval;
5. real deployment would require risk, compliance, fairness, explainability, consent, monitoring, and human review.

---

## 10. Business Interpretation

The project demonstrates how a financial-services analytics team can move from static campaign segmentation to a governed decision-ranking product. The main portfolio signal is not only model accuracy, but the ability to connect predictive modelling with commercial value, responsible credit behaviour, reproducible pipelines, dashboarding, and governance.
