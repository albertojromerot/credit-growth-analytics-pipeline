"""Dashboard entry point for the Credit Growth Analytics Pipeline."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"

st.set_page_config(page_title="Credit Growth Analytics Pipeline", layout="wide")

st.title("Credit Growth Analytics Pipeline")
st.caption("Responsible Customer Lifetime Value / Next-Best-Action Model")

ranking_path = DATA_DIR / "nba_ranked_customers.csv"
metrics_path = DATA_DIR / "model_metrics.csv"
benchmark_path = DATA_DIR / "benchmark_comparison.csv"

if not ranking_path.exists():
    st.warning(
        "Dashboard data has not been generated yet. Run `python -m src.run_pipeline` "
        "from the repository root, then refresh this dashboard."
    )
    st.stop()

ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])
metrics = pd.read_csv(metrics_path) if metrics_path.exists() else pd.DataFrame()
benchmark = pd.read_csv(benchmark_path) if benchmark_path.exists() else pd.DataFrame()

top_50 = ranking.nsmallest(50, "priority_rank")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest snapshot", str(ranking["snapshot_month"].max().date()))
col2.metric("Customers scored", f"{len(ranking):,}")
col3.metric("Top 50 expected value", f"£{top_50['expected_credit_value'].sum():,.0f}")
col4.metric("Top 50 eligible share", f"{top_50['eligible_for_responsible_offer'].mean():.0%}")

st.subheader("Top 50 Next-Best-Action list")
st.dataframe(
    top_50[[
        "priority_rank",
        "customer_id",
        "recommended_product",
        "p_conversion",
        "p_responsible",
        "expected_credit_value",
        "responsible_nba_score",
        "reason_codes",
        "recommended_action",
    ]],
    use_container_width=True,
    hide_index=True,
)

if not benchmark.empty:
    st.subheader("Benchmark comparison")
    st.dataframe(benchmark, use_container_width=True, hide_index=True)

if not metrics.empty:
    st.subheader("Model KPIs")
    st.dataframe(metrics, use_container_width=True, hide_index=True)
