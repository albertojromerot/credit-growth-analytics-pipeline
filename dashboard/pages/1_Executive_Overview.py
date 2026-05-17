"""Executive overview page."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.title("Executive Overview")
ranking_path = DATA_DIR / "nba_ranked_customers.csv"
segment_path = DATA_DIR / "segment_summary.csv"
if not ranking_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])
segment = pd.read_csv(segment_path) if segment_path.exists() else pd.DataFrame()
top_50 = ranking.nsmallest(50, "priority_rank")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Top 50 expected value", f"£{top_50['expected_credit_value'].sum():,.0f}")
col2.metric("Average conversion probability", f"{top_50['p_conversion'].mean():.1%}")
col3.metric("Average responsible-behaviour probability", f"{top_50['p_responsible'].mean():.1%}")
col4.metric("Governance exclusions in Top 50", int((~top_50["eligible_for_responsible_offer"].astype(bool)).sum()))

st.subheader("Recommended-product mix in Top 50")
product_mix = top_50.groupby("recommended_product", as_index=False).size()
st.plotly_chart(px.bar(product_mix, x="recommended_product", y="size", text="size"), use_container_width=True)

if not segment.empty:
    st.subheader("Segment summary")
    st.dataframe(segment, use_container_width=True, hide_index=True)
