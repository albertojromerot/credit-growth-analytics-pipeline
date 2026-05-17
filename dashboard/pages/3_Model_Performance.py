"""Model performance page."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.title("Model Performance")
metrics_path = DATA_DIR / "model_metrics.csv"
benchmark_path = DATA_DIR / "benchmark_comparison.csv"
if not metrics_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

metrics = pd.read_csv(metrics_path)
st.subheader("Model KPIs")
st.dataframe(metrics, use_container_width=True, hide_index=True)

metric_long = metrics.melt(
    id_vars=["model_name", "target"],
    value_vars=["roc_auc", "pr_auc", "brier_score", "precision_at_50", "precision_at_100"],
    var_name="metric",
    value_name="value",
)
st.plotly_chart(px.bar(metric_long, x="metric", y="value", color="model_name", barmode="group"), use_container_width=True)

if benchmark_path.exists():
    benchmark = pd.read_csv(benchmark_path)
    st.subheader("Targeting benchmark")
    st.dataframe(benchmark, use_container_width=True, hide_index=True)
