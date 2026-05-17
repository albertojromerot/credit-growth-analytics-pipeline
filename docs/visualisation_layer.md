# Visualisation Layer Draft

The visualisation layer is the asset equivalent of a Power BI dashboard.

The first implementation target is Streamlit because it can be reproduced directly from a public GitHub repository. The same layout can later be translated into Power BI.

## Dashboard Pages

### 1. Executive Overview

Purpose: communicate business value quickly.

Suggested visuals:

- total eligible customers;
- Top 50 expected value;
- action distribution;
- recommended product mix;
- benchmark comparison: rule-based vs model-based ranking.

### 2. Customer Ranking

Purpose: make the output advisor-ready.

Suggested visuals:

- ranked customer table;
- recommended product;
- responsible NBA score;
- `p_conversion`;
- `p_responsible`;
- expected value;
- reason codes;
- eligibility / exclusion flags.

### 3. Model Performance

Purpose: show analytical credibility.

Suggested visuals:

- ROC-AUC;
- PR-AUC;
- Precision@50;
- Lift@50;
- calibration view;
- comparison against manual segmentation.

### 4. Governance Monitoring

Purpose: show responsible, auditable modelling.

Suggested visuals:

- missingness summary;
- duplicate key checks;
- leakage checks;
- eligibility exclusions;
- drift indicators;
- treatment-log completeness.

## Design Principle

The dashboard should answer four questions:

1. Where is the commercial opportunity?
2. Which customers should be prioritised?
3. How well does the model perform?
4. Can the process be trusted and audited?
