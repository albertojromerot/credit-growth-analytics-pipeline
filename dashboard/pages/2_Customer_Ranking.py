"""Customer ranking page for the Next-Best-Action output."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.set_page_config(page_title="Customer Ranking", layout="wide")
st.title("Customer Ranking")
st.caption("Advisor-ready Next-Best-Action list with filters, reason codes, and governance flags.")

ranking_path = DATA_DIR / "nba_ranked_customers.csv"
if not ranking_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])

with st.sidebar:
    st.header("Filters")
    product = st.multiselect(
        "Recommended product",
        options=sorted(ranking["recommended_product"].dropna().unique()),
        default=sorted(ranking["recommended_product"].dropna().unique()),
    )
    segment = st.multiselect(
        "Customer segment",
        options=sorted(ranking["customer_segment"].dropna().unique()),
        default=sorted(ranking["customer_segment"].dropna().unique()),
    )
    eligible_only = st.checkbox("Eligible customers only", value=True)
    max_rank = st.slider("Show customers up to rank", 10, 250, 50, step=10)

filtered = ranking.loc[
    ranking["recommended_product"].isin(product)
    & ranking["customer_segment"].isin(segment)
    & ranking["priority_rank"].le(max_rank)
].copy()

if eligible_only:
    filtered = filtered.loc[filtered["eligible_for_responsible_offer"].astype(bool)].copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers shown", f"{len(filtered):,}")
col2.metric("Expected value", f"£{filtered['expected_credit_value'].sum():,.0f}")
col3.metric("Avg. conversion", f"{filtered['p_conversion'].mean():.1%}" if len(filtered) else "n/a")
col4.metric("Avg. responsible behaviour", f"{filtered['p_responsible'].mean():.1%}" if len(filtered) else "n/a")

st.subheader("Recommended action list")
st.dataframe(
    filtered[[
        "priority_rank",
        "customer_id",
        "recommended_product",
        "p_conversion",
        "p_responsible",
        "expected_credit_value",
        "responsible_nba_score",
        "eligible_for_responsible_offer",
        "governance_exclusion_reason",
        "reason_codes",
        "recommended_action",
        "customer_segment",
        "income_band",
        "region",
    ]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "p_conversion": st.column_config.ProgressColumn("p_conversion", format="%.1f", min_value=0, max_value=1),
        "p_responsible": st.column_config.ProgressColumn("p_responsible", format="%.1f", min_value=0, max_value=1),
        "expected_credit_value": st.column_config.NumberColumn("expected_credit_value", format="£%.0f"),
        "responsible_nba_score": st.column_config.NumberColumn("responsible_nba_score", format="%.1f"),
    },
)

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Score vs conversion probability")
    fig_scatter = px.scatter(
        filtered,
        x="p_conversion",
        y="responsible_nba_score",
        size="expected_credit_value",
        color="recommended_product",
        hover_data=["customer_id", "priority_rank", "p_responsible", "reason_codes"],
        title="Ranking logic: conversion probability and responsible NBA score",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with right:
    st.subheader("Reason-code frequency")
    if not filtered.empty:
        reasons = (
            filtered["reason_codes"]
            .str.split(" | ", regex=False)
            .explode()
            .value_counts()
            .reset_index()
        )
        reasons.columns = ["reason_code", "customers"]
        st.plotly_chart(
            px.bar(reasons.head(10), x="customers", y="reason_code", orientation="h", title="Top reason codes"),
            use_container_width=True,
        )
    else:
        st.info("No customers match the selected filters.")

st.info(
    "Use this page as the operational bridge between model output and advisor execution. "
    "The ranking should be reviewed by a human before any customer action."
)
