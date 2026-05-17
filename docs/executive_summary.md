# Executive Summary

## Responsible Credit Growth Through Next-Best-Action Analytics

This project demonstrates how a financial institution can prioritise credit-growth opportunities using a responsible and commercially focused analytics pipeline.

Instead of ranking customers only by their likelihood to accept an offer, the model combines three dimensions:

1. likelihood of conversion;
2. likelihood of responsible credit behaviour;
3. expected economic value.

The result is an advisor-ready ranked list that supports better campaign targeting, more focused commercial execution, and stronger governance.

---

## 1. Business Challenge

Commercial teams often need to decide which customers should receive a credit offer, which product should be suggested, and where advisor time should be focused. A purely manual approach can be slow, inconsistent, and difficult to validate.

A conversion-only model can also be incomplete: a customer may be likely to accept a loan, but that does not necessarily mean the opportunity is responsible, valuable, or suitable.

This project addresses that gap by ranking customers through a responsible value equation:

```text
Responsible NBA Score =
P(conversion) × P(responsible credit behaviour) × Expected Credit Value × Eligibility Rules
```

---

## 2. Solution

The repository implements a reproducible Python pipeline using synthetic financial-services data. The pipeline:

1. generates synthetic customer, behavioural, product, outcome, and treatment-log data;
2. creates a customer-month feature matrix;
3. trains two supervised models: conversion propensity and responsible behaviour;
4. estimates expected value by recommended credit product;
5. applies eligibility and responsible-lending filters;
6. produces a ranked Next-Best-Action list;
7. exports dashboard-ready data;
8. provides a Streamlit visualisation layer equivalent to a Power BI dashboard.

The output is designed for both technical review and non-technical business interpretation.

---

## 3. Current Synthetic Results

The model was validated against two benchmark alternatives: manual rule-based segmentation and a conversion-only model.

| Approach | Precision@50 conversion | Precision@50 responsible conversion | Expected value captured | Eligible share |
|---|---:|---:|---:|---:|
| Manual rule-based segmentation | 20% | 16% | £59,500 | 100% |
| Conversion-only model | 26% | 20% | £55,196 | 82% |
| Responsible NBA model | 24% | 22% | £59,500 | 100% |

The conversion-only model produced the highest raw conversion Precision@50. However, the Responsible NBA model produced the strongest responsible-conversion Precision@50 while maintaining expected value capture and applying eligibility discipline.

This is the central business point: the recommended approach is not simply optimising for loan uptake; it is balancing growth, behaviour quality, value, and governance.

---

## 4. Model Performance Snapshot

| Model | ROC-AUC | PR-AUC | Brier score | Precision@50 |
|---|---:|---:|---:|---:|
| Conversion model | 0.631 | 0.155 | 0.225 | 28% |
| Responsible behaviour model | 0.649 | 0.868 | 0.230 | 92% |

These are synthetic demonstration results. They should be interpreted as proof of pipeline design, validation logic, and decision-product thinking rather than real-world credit performance.

---

## 5. Business Value

The project shows how analytics can support commercial teams by:

- reducing manual segmentation effort;
- focusing advisor time on higher-priority customers;
- connecting model outputs to expected value;
- avoiding purely volume-driven credit targeting;
- applying responsible-lending exclusions before action;
- comparing rule-based segmentation against model-based ranking;
- creating dashboard-ready outputs for performance and governance monitoring.

---

## 6. Dashboard and Decision Outputs

The repository includes a visualisation layer with four pages:

1. **Executive Overview** — portfolio opportunity, expected value, and Top 50 summary.
2. **Customer Ranking** — ranked customers, recommended product, reason codes, and recommended action.
3. **Model Performance** — classification metrics, Precision@50, and benchmark comparison.
4. **Governance Monitoring** — data-quality checks, eligibility exclusions, and audit signals.

The key business output is not a model score by itself. It is an advisor-ready recommendation list that can be reviewed, acted on, and monitored.

---

## 7. Governance Positioning

The model is designed for decision support, not automated credit approval.

It includes:

- synthetic data only;
- time-ordered validation;
- leakage checks;
- duplicate-key checks;
- missingness monitoring;
- eligibility filters;
- responsible-lending exclusions;
- model-card documentation;
- treatment-log structure for future intervention learning.

In a real financial-services environment, final action would still require affordability assessment, risk policy, compliance review, fair-treatment controls, consent management, and human oversight.

---

## 8. Employer-Facing Positioning

This asset is relevant to finance and analytics scenarios because it connects:

- customer analytics;
- credit risk awareness;
- commercial prioritisation;
- BI/dashboard thinking;
- reproducible Python pipelines;
- governance and responsible lending;
- model validation beyond generic accuracy.

The project demonstrates the ability to translate a business problem into an auditable analytics product that supports measurable commercial decision-making.
