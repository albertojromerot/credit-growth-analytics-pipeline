# Technical Note Draft

## 1. Business Problem

Financial institutions need to identify customers who are suitable for credit-growth actions while balancing conversion, risk, value, and responsible lending considerations.

This project builds a reproducible Next-Best-Action pipeline that ranks customers using:

```text
P(conversion) × P(responsible credit behaviour) × Expected Credit Value
```

## 2. Data

The repository uses synthetic data only. The planned schema includes customer-level attributes, monthly behavioural signals, credit-product assumptions, historical conversion labels, responsible behaviour labels, and a sample treatment log.

## 3. Modelling

The modelling layer contains three components:

1. conversion propensity model;
2. responsible credit behaviour model;
3. expected value calculation.

The final score is used to generate a prioritised customer list with recommended product, action, reason codes, and governance flags.

## 4. Validation

The project compares rule-based segmentation, a conversion-only model, and the Responsible NBA model.

Planned metrics include ROC-AUC, PR-AUC, Precision@50, Lift@50, Brier Score, expected value captured, and monthly stability.

## 5. Governance

The pipeline includes checks for leakage, duplicate customer-month keys, missingness, eligibility, responsible lending exclusions, and drift monitoring.

The model supports decision intelligence and prioritisation. It does not automate final credit approval.
