# Reproducibility and Validation Guide

This guide explains how a reviewer can validate the repository and view the final dashboard results from a clean terminal session.

Run all commands from the repository root. The repository root is the folder that contains `README.md`, `requirements.txt`, `src`, `dashboard`, `data`, `docs`, and `tests`.

## 1. Confirm the working folder

```bash
pwd
ls
```

You should see:

```text
README.md
requirements.txt
src
dashboard
data
docs
tests
```

## 2. Create a local Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. Run the full pipeline

```bash
python -m src.run_pipeline
```

This executes:

1. synthetic data generation;
2. feature construction;
3. model training;
4. customer scoring;
5. benchmark comparison;
6. governance checks;
7. dashboard-ready exports.

Expected final terminal message:

```text
Pipeline completed. Check the outputs/ and dashboard/data/ folders.
```

## 4. Run automated tests

```bash
python -m pytest tests -q
```

Expected result:

```text
4 passed
```

## 5. View the final dashboard results

```bash
python -m streamlit run dashboard/streamlit_app.py
```

The dashboard is the final visual output of the ML/AI pipeline. It provides a Power BI-style layer with:

1. Main Dashboard;
2. Executive Overview;
3. Customer Ranking;
4. Model Performance;
5. Governance Monitoring.

A non-technical reviewer should start with the Main Dashboard and Executive Overview. A technical reviewer should also inspect Model Performance and Governance Monitoring.

## 6. Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `No such file or directory: requirements.txt` | Wrong folder | Move into the folder that contains `requirements.txt` |
| `No module named 'src'` | Pipeline run from the wrong folder | Run `python -m src.run_pipeline` from the repository root |
| `PermissionError` during pytest collection | Tests run from a parent folder | Run `python -m pytest tests -q` from the repository root |
| Streamlit cannot find the app file | Wrong folder | Run the Streamlit command from the repository root |
