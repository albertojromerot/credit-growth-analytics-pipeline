# ML/AI Model Specification

## 1. Purpose

This document describes the current machine learning specification for the Credit Growth Analytics Pipeline.

The repository implements a responsible credit-growth Next-Best-Action system. The objective is not to automate credit approval. The objective is to prioritise customers for suitable commercial review by combining:

```text
P(conversion) × P(responsible credit behaviour) × Expected Credit Value × Eligibility Rules
```

---

## 2. Current Implemented Model

The current implemented classifier is:

```text
sklearn.ensemble.ExtraTreesClassifier
```

It is wrapped inside a scikit-learn `Pipeline` with preprocessing.

The choice of Extra Trees is suitable for this portfolio version because it is:

1. robust for mixed numerical and categorical tabular features after encoding;
2. relatively fast to train;
3. able to capture non-linear interactions;
4. less sensitive to monotonic transformations than linear models;
5. useful as a strong, reproducible tabular benchmark.

A HistGradientBoostingClassifier is a strong candidate for a future model comparison layer, but it is not the current implemented champion in this repository. The current repository should describe the implemented model as Extra Trees unless the code is later changed.

---

## 3. Modelling Components

| Component | Target / output | Model type | Purpose |
|---|---|---|---|
| Conversion model | `converted_next_3m` | Extra Trees classifier | Estimate probability of customer conversion |
| Responsible behaviour model | `responsible_credit_behaviour_6m` | Extra Trees classifier | Estimate probability of responsible credit behaviour |
| Expected value layer | `expected_credit_value` | Deterministic product-value calculation | Estimate commercial value by recommended product |
| Ranking layer | `responsible_nba_score` | Business scoring equation | Rank customers for Next-Best-Action review |

---

## 4. Classifier Hyperparameters

Current classifier configuration:

| Parameter | Value | Rationale |
|---|---:|---|
| `n_estimators` | 120 | stable ensemble size for the synthetic portfolio scale |
| `max_depth` | 9 | limits complexity and reduces overfitting risk |
| `min_samples_leaf` | 25 | smooths terminal leaves and improves generalisation |
| `class_weight` | `balanced` | accounts for imbalanced target rates |
| `random_state` | 42 | reproducibility |
| `n_jobs` | -1 | parallel training |

---

## 5. Preprocessing Pipeline

The model uses a scikit-learn `ColumnTransformer`.

| Feature type | Transformation |
|---|---|
| Numeric features | median imputation |
| Categorical features | most-frequent imputation + one-hot encoding |
| Unlisted fields | dropped from the model matrix |

The one-hot encoder uses `handle_unknown='ignore'`, which allows the scoring pipeline to handle categories not observed during training.

---

## 6. Governed Feature Set

The current model uses 21 features:

| Feature group | Features |
|---|---|
| Profile | `age`, `tenure_months`, `annual_income`, `income_band_score` |
| Engagement | `digital_engagement_score`, `engagement_score`, `salary_inflow_flag` |
| Financial behaviour | `savings_balance`, `credit_balance`, `recent_balance_growth` |
| Credit exposure | `utilisation_ratio`, `arrears_last_6m`, `credit_to_income_ratio` |
| Relationship depth | `number_of_products`, `product_depth_score` |
| Affordability | `affordability_proxy`, `balance_to_income_ratio` |
| Categorical context | `region`, `employment_type`, `customer_segment` |
| Recent enquiry | `recent_credit_enquiry_flag` |

The feature list is defined centrally in `src/config.py` to keep training and scoring consistent.

---

## 7. Temporal Validation

The repository uses a time-ordered train/test split. The test set uses the latest labelled months with at least one positive label for the selected target.

This avoids an uninformative validation period where the latest month has no positive observations.

Current split outputs:

| Model | Train rows | Test rows | Train positive rate | Test positive rate |
|---|---:|---:|---:|---:|
| Conversion model | 18,000 | 3,600 | 8.71% | 8.83% |
| Responsible behaviour model | 18,000 | 3,600 | 80.07% | 80.44% |

---

## 8. Current Model Metrics

| Model | Target | ROC-AUC | PR-AUC | Brier score | Precision@50 | Precision@100 |
|---|---|---:|---:|---:|---:|---:|
| Conversion model | `converted_next_3m` | 0.631 | 0.155 | 0.225 | 28% | 27% |
| Responsible behaviour model | `responsible_credit_behaviour_6m` | 0.649 | 0.868 | 0.230 | 92% | 90% |

These metrics are generated from synthetic data and should be treated as demonstration outputs, not real-world credit-risk evidence.

---

## 9. Responsible NBA Scoring

After both models generate probabilities, the scoring layer selects a recommended product and calculates:

```text
responsible_nba_score =
p_conversion × p_responsible × expected_credit_value × eligible_for_responsible_offer
```

Eligibility rules set the score to zero where customers fail responsible-lending guardrails.

Current eligibility exclusions include:

1. recent arrears signal;
2. utilisation ratio above 90%;
3. no stable income signal;
4. annual income below the portfolio threshold.

---

## 10. Benchmark Comparison

The validation layer compares three targeting approaches:

| Approach | Precision@50 conversion | Precision@50 responsible conversion | Expected value captured | Eligible share |
|---|---:|---:|---:|---:|
| Manual rule-based segmentation | 20% | 16% | £59,500 | 100% |
| Conversion-only model | 26% | 20% | £55,196 | 82% |
| Responsible NBA model | 24% | 22% | £59,500 | 100% |

The Responsible NBA model is positioned as the preferred decision approach because it balances conversion, responsible behaviour, expected value, and eligibility discipline.

---

## 11. Model Artefacts

The pipeline saves trained model artefacts to:

```text
outputs/models/conversion_model.joblib
outputs/models/responsible_behaviour_model.joblib
```

It also exports dashboard-ready metrics to:

```text
dashboard/data/model_metrics.csv
dashboard/data/benchmark_comparison.csv
dashboard/data/nba_ranked_customers.csv
dashboard/data/governance_checks.csv
```

---

## 12. Candidate Future Enhancements

Future versions may add:

1. HistGradientBoostingClassifier as a challenger model;
2. Logistic Regression as an interpretable baseline;
3. calibration curves and probability calibration;
4. SHAP or permutation importance for richer explainability;
5. uplift modelling once treatment-log outcomes exist;
6. fairness and segment-performance diagnostics;
7. model registry-style artefact tracking;
8. automated GitHub Actions validation.

---

## 13. Deployment and Governance Position

This model is designed for demonstration and decision support. In a real financial institution, final usage would require:

1. formal affordability assessment;
2. credit risk policy approval;
3. compliance and fair-treatment review;
4. consent and data-protection controls;
5. human review before customer contact;
6. post-deployment monitoring;
7. intervention logging and outcome measurement.
