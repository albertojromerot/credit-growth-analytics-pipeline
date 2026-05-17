"""Executive overview page for the portfolio dashboard."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TOP_N = 50

st.set_page_config(page_title="Executive Overview", layout="wide")
st.title("Executive Overview")
st.caption("Commercial opportunity, responsible eligibility, and product mix for the Top 50 action pool.")

ranking_path = DATA_DIR / "nba_ranked_customers.csv"
segment_path = DATA_DIR / "segment_summary.csv"
benchmark_path = DATA_DIR / "benchmark_comparison.csv"

if not ranking_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])
segment = pd.read_csv(segment_path) if segment_path.exists() else pd.DataFrame()
benchmark = pd.read_csv(benchmark_path) if benchmark_path.exists() else pd.DataFrame()
top_50 = ranking.nsmallest(TOP_N, "priority_rank")

st.markdown(
    """
This page is designed for a non-technical decision maker. It shows the size of the prioritised opportunity,
the expected-value proxy, the recommended product mix, and the business interpretation of the Top 50 list.
"""
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Top 50 expected value", f"£{top_50['expected_credit_value'].sum():,.0f}")
col2.metric("Average conversion probability", f"{top_50['p_conversion'].mean():.1%}")
col3.metric("Average responsible-behaviour probability", f"{top_50['p_responsible'].mean():.1%}")
col4.metric("Governance exclusions in Top 50", int((~top_50["eligible_for_responsible_offer"].astype(bool)).sum()))

st.divider()

left, right = st.columns([1, 1])
with left:
    st.subheader("Recommended-product mix in Top 50")
    product_mix = top_50.groupby("recommended_product", as_index=False).agg(customers=("customer_id", "count"))
    fig_product = px.bar(
        product_mix.sort_values("customers", ascending=False),
        x="recommended_product",
        y="customers",
        text="customers",
        title="Number of recommended actions by product",
    )
    st.plotly_chart(fig_product, use_container_width=True)

with right:
    st.subheader("Expected value by customer segment")
    segment_value = top_50.groupby("customer_segment", as_index=False).agg(
        customers=("customer_id", "count"),
        expected_value=("expected_credit_value", "sum"),
    )
    fig_segment = px.bar(
        segment_value.sort_values("expected_value", ascending=False),
        x="customer_segment",
        y="expected_value",
        text_auto=".2s",
        title="Expected value captured in Top 50",
    )
    st.plotly_chart(fig_segment, use_container_width=True)

st.subheader("Business reading")
st.markdown(
    """
- The Top 50 list should be treated as an **advisor action pool**, not an automated approval list.
- The responsible NBA score favours customers who combine conversion likelihood, responsible-behaviour probability, expected value, and eligibility.
- The output is designed to reduce manual segmentation effort while keeping governance checks visible.
"""
)

if not benchmark.empty:
    st.subheader("Executive benchmark")
    benchmark_display = benchmark.copy()
    st.dataframe(benchmark_display, use_container_width=True, hide_index=True)

if not segment.empty:
    st.subheader("Segment summary")
    st.dataframe(segment, use_container_width=True, hide_index=True)
