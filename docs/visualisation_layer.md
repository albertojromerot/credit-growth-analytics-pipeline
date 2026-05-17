# Visualisation Layer

The visualisation layer is implemented in Streamlit and is the final dashboard output of the Credit Growth Analytics Pipeline.

It is designed as the equivalent of a Power BI dashboard: a reviewer can inspect the business opportunity, customer ranking, model performance, and governance controls without reading every source-code file.

## How to launch the dashboard

Run the pipeline first from the repository root:

```bash
python -m src.run_pipeline
```

Then launch the dashboard:

```bash
python -m streamlit run dashboard/streamlit_app.py
```

## Implemented dashboard pages

### 1. Main Dashboard

Purpose: provide a fast executive entry point.

Includes:

- latest snapshot;
- customers scored;
- Top 50 expected value;
- Top 50 average conversion probability;
- Top 50 eligible share;
- Top 10 recommendations;
- product mix;
- priority-score distribution;
- benchmark comparison;
- model KPI snapshot;
- governance check status.

### 2. Executive Overview

Purpose: communicate business value quickly to non-technical reviewers.

Includes:

- Top 50 expected value;
- average conversion probability;
- average responsible-behaviour probability;
- governance exclusions in the Top 50;
- recommended-product mix;
- expected value by customer segment;
- executive benchmark table;
- segment summary.

### 3. Customer Ranking

Purpose: make the output advisor-ready.

Includes:

- sidebar filters by product and customer segment;
- eligible-only toggle;
- rank slider;
- customer-level ranking table;
- recommended product;
- responsible NBA score;
- `p_conversion`;
- `p_responsible`;
- expected credit value;
- reason codes;
- recommended action;
- score-vs-conversion scatter chart;
- reason-code frequency chart.

### 4. Model Performance

Purpose: show analytical credibility.

Includes:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Precision@50;
- Precision@100;
- model KPI table;
- model-metric comparison chart;
- targeting benchmark;
- expected-value comparison.

### 5. Governance Monitoring

Purpose: show responsible, auditable modelling.

Includes:

- pass/review counters;
- data-quality checks;
- duplicate-key checks;
- leakage checks;
- responsible-lending exclusion distribution;
- Top 50 governance review table;
- audit notes for future institutional deployment.

## Design principle

The dashboard answers four questions:

1. Where is the commercial opportunity?
2. Which customers should be prioritised?
3. How well does the model perform?
4. Can the process be trusted and audited?

## Screenshot assets

Screenshots should be saved in:

```text
docs/assets/screenshots/
```

Recommended files:

```text
01_dashboard_landing.png
02_executive_overview.png
03_customer_ranking.png
04_model_performance.png
05_governance_monitoring.png
```

After the screenshots are uploaded, they should be embedded in the main `README.md` so that a recruiter can preview the dashboard without running the app locally.
