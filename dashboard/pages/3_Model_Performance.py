"""Model performance page for the portfolio dashboard."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.set_page_config(page_title="Model Performance", layout="wide")
st.title("Model Performance")
st.caption("Classification metrics, ranking metrics, and targeting benchmark comparison.")

metrics_path = DATA_DIR / "model_metrics.csv"
benchmark_path = DATA_DIR / "benchmark_comparison.csv"

if not metrics_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

metrics = pd.read_csv(metrics_path)
benchmark = pd.read_csv(benchmark_path) if benchmark_path.exists() else pd.DataFrame()

st.markdown(
    """
This page separates **model quality** from **business ranking quality**. The classification models estimate conversion and
responsible-behaviour probabilities; the benchmark compares how different targeting strategies perform in the Top 50 action pool.
"""
)

col1, col2, col3, col4 = st.columns(4)
conversion = metrics.loc[metrics["model_name"].eq("conversion_model")].iloc[0]
responsible = metrics.loc[metrics["model_name"].eq("responsible_behaviour_model")].iloc[0]
col1.metric("Conversion ROC-AUC", f"{conversion['roc_auc']:.3f}")
col2.metric("Conversion Precision@50", f"{conversion['precision_at_50']:.0%}")
col3.metric("Responsible ROC-AUC", f"{responsible['roc_auc']:.3f}")
col4.metric("Responsible Precision@50", f"{responsible['precision_at_50']:.0%}")

st.subheader("Model KPI table")
st.dataframe(
    metrics,
    use_container_width=True,
    hide_index=True,
    column_config={
        "roc_auc": st.column_config.NumberColumn("roc_auc", format="%.3f"),
        "pr_auc": st.column_config.NumberColumn("pr_auc", format="%.3f"),
        "brier_score": st.column_config.NumberColumn("brier_score", format="%.3f"),
        "precision_at_50": st.column_config.NumberColumn("precision_at_50", format="%.0%"),
        "precision_at_100": st.column_config.NumberColumn("precision_at_100", format="%.0%"),
    },
)

metric_long = metrics.melt(
    id_vars=["model_name", "target"],
    value_vars=["roc_auc", "pr_auc", "brier_score", "precision_at_50", "precision_at_100"],
    var_name="metric",
    value_name="value",
)
fig_metrics = px.bar(
    metric_long,
    x="metric",
    y="value",
    color="model_name",
    barmode="group",
    text_auto=".2f",
    title="Model metrics by component",
)
st.plotly_chart(fig_metrics, use_container_width=True)

if not benchmark.empty:
    st.divider()
    st.subheader("Targeting benchmark")
    st.markdown(
        """
The benchmark shows why the responsible NBA ranking is different from a conversion-only model: it balances conversion,
responsible behaviour, expected value, and eligibility discipline.
"""
    )
    st.dataframe(
        benchmark,
        use_container_width=True,
        hide_index=True,
        column_config={
            "precision_at_50_conversion": st.column_config.NumberColumn("precision_at_50_conversion", format="%.0%"),
            "precision_at_50_responsible_conversion": st.column_config.NumberColumn("precision_at_50_responsible_conversion", format="%.0%"),
            "expected_value_captured": st.column_config.NumberColumn("expected_value_captured", format="£%.0f"),
            "eligible_share": st.column_config.NumberColumn("eligible_share", format="%.0%"),
        },
    )

    benchmark_long = benchmark.melt(
        id_vars=["approach"],
        value_vars=[
            "precision_at_50_conversion",
            "precision_at_50_responsible_conversion",
            "eligible_share",
        ],
        var_name="metric",
        value_name="value",
    )
    fig_benchmark = px.bar(
        benchmark_long,
        x="metric",
        y="value",
        color="approach",
        barmode="group",
        text_auto=".0%",
        title="Top 50 targeting comparison",
    )
    fig_benchmark.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_benchmark, use_container_width=True)

    fig_value = px.bar(
        benchmark,
        x="approach",
        y="expected_value_captured",
        text_auto=".2s",
        title="Expected value captured by targeting approach",
    )
    st.plotly_chart(fig_value, use_container_width=True)

st.info(
    "The results use synthetic data. They demonstrate modelling, validation, and decision-product design rather than real credit-risk performance."
)
