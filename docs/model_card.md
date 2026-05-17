# Model Card

## Model Name

Responsible Credit Next-Best-Action Model

## Purpose

Prioritise customers for suitable credit-growth actions by combining conversion propensity, responsible credit behaviour, and expected value.

## Intended Use

This model is intended for customer analytics, campaign prioritisation, and commercial decision support in a financial-services context.

It is not intended to automate credit approval or replace formal affordability, risk, compliance, or underwriting processes.

## Data

The public repository uses synthetic data only.

Planned data domains:

- customer attributes;
- monthly behavioural signals;
- product catalogue and value assumptions;
- historical conversion outcomes;
- responsible credit behaviour outcomes;
- treatment-log sample.

## Targets

| Target | Description |
|---|---|
| `converted_next_3m` | Whether the customer converted into a credit product within the next 3 months |
| `responsible_credit_behaviour_6m` | Whether the customer showed responsible behaviour after conversion |

## Main Score

```text
responsible_nba_score =
p_conversion × p_responsible × expected_value
```

## Validation

Planned validation:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Precision@50;
- Lift@50;
- expected value captured;
- monthly stability;
- leakage checks.

## Governance

Planned checks:

- temporal split validation;
- missingness checks;
- duplicate key checks;
- high-risk exclusion;
- eligibility filters;
- model drift monitoring;
- reason-code review.

## Limitations

- Synthetic data does not represent a real institution.
- Results are for demonstration and portfolio purposes.
- Expected value assumptions are simplified.
- Human review remains required before any customer action.

## Ethical Considerations

The model prioritises responsible credit growth and should avoid promoting unsuitable lending. It must be combined with affordability checks, risk controls, fair treatment principles, and appropriate customer consent processes.
