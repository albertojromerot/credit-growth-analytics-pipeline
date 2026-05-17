# Implementation Status

## Current implementation phase

The repository now includes a reproducible core pipeline for the portfolio project:

1. synthetic customer and credit-product data generation;
2. feature matrix construction;
3. conversion and responsible-behaviour models;
4. responsible Next-Best-Action scoring;
5. benchmark comparison against manual segmentation and conversion-only ranking;
6. governance checks;
7. dashboard-ready CSV exports;
8. Streamlit dashboard pages.

## Main command

Run from the repository root:

```bash
python -m src.run_pipeline
```

Then launch the dashboard:

```bash
streamlit run dashboard/streamlit_app.py
```

## Note

The project uses synthetic data only. It is designed as a public asset and not as an automated credit approval system.
