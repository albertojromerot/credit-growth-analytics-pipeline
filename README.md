# Credit Growth Analytics Pipeline

## Responsible Customer Lifetime Value / Next-Best-Action Model

This repository is a portfolio-ready analytics project that demonstrates how customer analytics, responsible credit behaviour modelling, and expected value estimation can be combined into an auditable **Next-Best-Action** decision pipeline for financial services.

The goal is not only to predict who is likely to convert. The goal is to prioritise customers who are likely to:

1. accept a suitable credit offer;
2. show responsible credit behaviour after conversion; and
3. generate sustainable expected value for the business.

```text
Responsible NBA Score =
P(conversion)
× P(responsible credit behaviour)
× Expected Credit Value
× Eligibility / governance filters
```

---

## 1. Business Problem

Financial institutions need to grow their credit portfolios while protecting customers, controlling risk, and focusing commercial teams on the most valuable opportunities.

Traditional campaign segmentation often relies on static rules such as income band, tenure, age group, or current product ownership. This project reframes the problem as a governed decision-ranking system:

> Which customer should receive which next-best credit action, based on conversion likelihood, responsible credit behaviour, expected value, and eligibility rules?

---

## 2. Portfolio Relevance

This project is designed for London-based finance, analytics, BI, customer analytics, credit risk, and commercial data science roles.

It demonstrates the ability to:

- translate a commercial problem into an analytical decision system;
- build a reproducible Python pipeline;
- generate safe synthetic financial-services data;
- validate models using ranking and business metrics, not only accuracy;
- design a visualisation layer equivalent to a Power BI dashboard;
- document governance, responsible lending filters, and monitoring requirements.

---

## 3. Solution Overview

The pipeline contains five main layers:

| Layer | Purpose | Example Output |
|---|---|---|
| Synthetic data layer | Safe customer, behaviour, product, and outcome data | `customers.csv`, `monthly_behaviour.csv` |
| Feature engineering layer | Build customer-month predictive features | product depth, balance trends, engagement |
| Modelling layer | Estimate conversion and responsible behaviour | `p_conversion`, `p_responsible` |
| Value and ranking layer | Combine probabilities with expected value | `responsible_nba_score` |
| Visualisation layer | Executive and analytical dashboards | ranking, value, governance, performance |

---

## 4. Repository Structure

```text
credit-growth-analytics-pipeline/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── synthetic/
│       ├── customers.csv
│       ├── monthly_behaviour.csv
│       ├── credit_products.csv
│       ├── credit_outcomes.csv
│       └── treatment_log_sample.csv
│
├── notebooks/
│   ├── 01_generate_synthetic_data.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modelling_conversion_risk_value.ipynb
│   ├── 05_next_best_action_ranking.ipynb
│   └── 06_model_validation_governance.ipynb
│
├── src/
│   ├── config.py
│   ├── data_generation.py
│   ├── preprocessing.py
│   ├── features.py
│   ├── modelling.py
│   ├── scoring.py
│   ├── validation.py
│   └── governance.py
│
├── dashboard/
│   ├── README.md
│   ├── streamlit_app.py
│   ├── assets/
│   ├── data/
│   └── pages/
│       ├── 1_Executive_Overview.py
│       ├── 2_Customer_Ranking.py
│       ├── 3_Model_Performance.py
│       └── 4_Governance_Monitoring.py
│
├── outputs/
│   ├── model_metrics.csv
│   ├── nba_ranked_customers.csv
│   ├── segment_summary.csv
│   ├── validation_summary.csv
│   └── governance_checks.csv
│
├── docs/
│   ├── architecture_diagram.md
│   ├── executive_summary.md
│   ├── technical_note.md
│   ├── model_card.md
│   └── visualisation_layer.md
│
└── tests/
    ├── test_features.py
    ├── test_scoring.py
    └── test_no_leakage.py
```

---

## 5. Synthetic Data Design

The project uses synthetic data only. No real customer data is included.

Planned synthetic tables:

| Table | Purpose |
|---|---|
| `customers.csv` | Customer demographics and static attributes |
| `monthly_behaviour.csv` | Customer-month behavioural signals |
| `credit_products.csv` | Product catalogue and expected value assumptions |
| `credit_outcomes.csv` | Historical conversion and responsible behaviour labels |
| `treatment_log_sample.csv` | Sample intervention tracking for future learning |

---

## 6. Modelling Approach

The analytical design uses three complementary components:

### 6.1. Conversion Propensity

Predicts the probability that a customer accepts or converts into a suitable credit product.

```text
p_conversion = P(customer converts within next 3 months)
```

### 6.2. Responsible Credit Behaviour

Predicts the probability that the customer behaves responsibly after conversion.

```text
p_responsible = P(no serious deterioration / arrears within next 6 months)
```

### 6.3. Expected Credit Value

Estimates expected value by customer and product, using assumptions such as expected amount, margin, cost, and expected loss.

```text
expected_value = expected_revenue - funding_cost - operating_cost - expected_loss
```

### 6.4. Final Ranking Score

```text
responsible_nba_score =
p_conversion × p_responsible × expected_value
```

The final output is an advisor-ready ranked list with recommended action, reason codes, and governance flags.

---

## 7. Validation Strategy

The project will compare three approaches:

| Approach | Description |
|---|---|
| Rule-based segmentation | Manual logic based on income, tenure, product ownership, or balance |
| Conversion-only model | Ranks customers by probability of accepting an offer |
| Responsible NBA model | Ranks by conversion × responsible behaviour × expected value |

Planned metrics:

| Category | Metrics |
|---|---|
| Classification | ROC-AUC, PR-AUC, Brier Score |
| Ranking | Precision@50, Recall@50, Lift@50 |
| Business value | Expected value captured in Top 50 |
| Governance | Leakage checks, missingness checks, eligibility filters |
| Stability | Monthly performance and drift monitoring |

---

## 8. Visualisation Layer

The repository includes a dashboard layer designed as the portfolio equivalent of a Power BI dashboard.

The dashboard will present:

1. **Executive Overview**  
   Portfolio opportunity, expected value, Top 50 customer summary, and action distribution.

2. **Customer Ranking**  
   Ranked Next-Best-Action list with probabilities, score, recommended product, reason codes, and eligibility flags.

3. **Model Performance**  
   ROC-AUC, PR-AUC, Precision@50, Lift@50, calibration, and benchmark comparison.

4. **Governance Monitoring**  
   Data quality checks, missingness, leakage tests, model drift, and responsible lending exclusions.

The initial implementation target is a Streamlit dashboard because it is easy to reproduce inside a public GitHub portfolio. The design can later be translated into Power BI.

---

## 9. Governance and Responsible Lending

This project includes a governance layer covering:

- temporal train/test splitting;
- leakage prevention;
- customer eligibility filters;
- responsible lending exclusions;
- missingness checks;
- duplicate customer-month key checks;
- model-card documentation;
- treatment-log feedback loop;
- monitoring and drift checks.

The model is intended to support prioritisation and decision intelligence. It is not intended to automate final credit approval.

---

## 10. How to Run the Project

The implementation will be added progressively.

Planned setup:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

Planned execution flow:

```bash
python src/data_generation.py
python src/features.py
python src/modelling.py
python src/scoring.py
python src/validation.py
streamlit run dashboard/streamlit_app.py
```

---

## 11. Expected Outputs

| Output | Purpose |
|---|---|
| `outputs/model_metrics.csv` | Model and benchmark KPIs |
| `outputs/nba_ranked_customers.csv` | Advisor-ready customer ranking |
| `outputs/segment_summary.csv` | Segment-level business interpretation |
| `outputs/validation_summary.csv` | Validation and performance summary |
| `outputs/governance_checks.csv` | Audit and governance results |

---

## 12. Documentation

| Document | Purpose |
|---|---|
| `docs/technical_note.md` | 1–2 page technical explanation |
| `docs/executive_summary.md` | 1-page non-technical summary |
| `docs/model_card.md` | Purpose, limitations, validation, governance |
| `docs/architecture_diagram.md` | Mermaid architecture diagram |
| `docs/visualisation_layer.md` | Dashboard design and KPI layout |

---

## 13. Status

Current status: repository blueprint and documentation scaffold.

Next implementation steps:

1. finalise synthetic data schema;
2. generate reproducible synthetic data;
3. build feature engineering pipeline;
4. train benchmark models;
5. create the responsible NBA score;
6. build dashboard pages;
7. write technical note and executive summary;
8. update CV and LinkedIn once results are final.
