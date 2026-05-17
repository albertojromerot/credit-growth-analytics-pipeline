# Model Card

## Model Name

Responsible Credit Next-Best-Action Model

## Purpose

Prioritise customers for suitable credit-growth actions by combining conversion propensity, responsible credit behaviour, expected value, and eligibility rules.

The model supports commercial decision intelligence. It does not automate credit approval.

---

## Intended Use

This model is intended for:

- customer analytics;
- campaign prioritisation;
- credit-growth opportunity ranking;
- commercial decision support;
- dashboard-based monitoring;
- portfolio analytics demonstrations.

It is not intended to replace formal affordability, risk, compliance, underwriting, or human-review processes.

---

## Data

The public repository uses synthetic data only.

Data domains:

- customer attributes;
- monthly behavioural signals;
- product catalogue and value assumptions;
- historical conversion outcomes;
- responsible credit behaviour outcomes;
- treatment-log sample.

No real customer or institutional data is included.

---

## Targets

| Target | Description |
|---|---|
| `converted_next_3m` | Whether the customer converted into a credit product within the next 3 months |
| `responsible_credit_behaviour_6m` | Whether the customer showed responsible credit behaviour in the following 6 months |

---

## Model Specification

The current implemented classifier is:

```text
sklearn.ensemble.ExtraTreesClassifier
```

The classifier is wrapped inside a scikit-learn `Pipeline` with numeric imputation and categorical one-hot encoding.

Current classifier parameters:

| Parameter | Value |
|---|---:|
| `n_estimators` | 120 |
| `max_depth` | 9 |
| `min_samples_leaf` | 25 |
| `class_weight` | `balanced` |
| `random_state` | 42 |
| `n_jobs` | -1 |

Full specification: [`docs/ml_model_specification.md`](ml_model_specification.md).

---

## Main Score

```text
responsible_nba_score =
p_conversion × p_responsible × expected_credit_value × eligible_for_responsible_offer
```

Eligibility rules set the score to zero when a customer fails responsible-lending guardrails.

---

## Validation

Current synthetic model metrics:

| Model | Target | ROC-AUC | PR-AUC | Brier score | Precision@50 |
|---|---|---:|---:|---:|---:|
| Conversion model | `converted_next_3m` | 0.631 | 0.155 | 0.225 | 28% |
| Responsible behaviour model | `responsible_credit_behaviour_6m` | 0.649 | 0.868 | 0.230 | 92% |

Benchmark comparison:

| Approach | Precision@50 conversion | Precision@50 responsible conversion | Expected value captured | Eligible share |
|---|---:|---:|---:|---:|
| Manual rule-based segmentation | 20% | 16% | £59,500 | 100% |
| Conversion-only model | 26% | 20% | £55,196 | 82% |
| Responsible NBA model | 24% | 22% | £59,500 | 100% |

Results are synthetic demonstration outputs, not real credit-risk performance evidence.

---

## Governance

Implemented or documented checks include:

- temporal train/test split;
- missingness checks;
- duplicate customer-month key checks;
- leakage-oriented tests;
- high-risk exclusion logic;
- eligibility filters;
- responsible-lending exclusions;
- model-card documentation;
- dashboard-ready governance monitoring;
- treatment-log structure for future learning.

---

## Limitations

- Synthetic data does not represent a real institution.
- Results are for demonstration purposes.
- Expected value assumptions are simplified.
- Eligibility rules are illustrative.
- Human review remains required before customer action.
- A real implementation would require fairness, affordability, compliance, consent, monitoring, and risk-policy review.

---

## Ethical Considerations

The model prioritises responsible credit growth and should avoid promoting unsuitable lending. It must be combined with affordability checks, risk controls, fair treatment principles, appropriate customer consent processes, and human oversight.
