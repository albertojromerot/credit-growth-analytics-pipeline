# Reproducibility and Validation Guide

This guide explains how a reviewer can validate the repository from a clean terminal session.

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

This executes synthetic data generation, feature construction, model training, scoring, benchmark comparison, governance checks, and dashboard-ready exports.

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

## 5. Launch the dashboard

```bash
python -m streamlit run dashboard/streamlit_app.py
```

The dashboard provides a Power BI-style visualisation layer with executive overview, customer ranking, model performance, and governance monitoring.

## 6. Troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `No such file or directory: requirements.txt` | Wrong folder | Move into the folder that contains `requirements.txt` |
| `No module named 'src'` | Pipeline run from the wrong folder | Run `python -m src.run_pipeline` from the repository root |
| `PermissionError` during pytest collection | Tests run from a parent folder | Run `python -m pytest tests -q` from the repository root |
| Streamlit cannot find the app file | Wrong folder | Run the Streamlit command from the repository root |

## 7. Reviewer checklist

A reviewer should be able to confirm that the project installs, the pipeline runs end to end, tests pass, the dashboard launches, and the documentation explains the business problem, modelling logic, governance, and limitations.
