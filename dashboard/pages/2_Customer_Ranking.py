"""Customer ranking page."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.title("Customer Ranking")
ranking_path = DATA_DIR / "nba_ranked_customers.csv"
if not ranking_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])
product = st.multiselect(
    "Recommended product",
    options=sorted(ranking["recommended_product"].unique()),
    default=sorted(ranking["recommended_product"].unique()),
)
segment = st.multiselect(
    "Customer segment",
    options=sorted(ranking["customer_segment"].unique()),
    default=sorted(ranking["customer_segment"].unique()),
)
max_rank = st.slider("Show customers up to rank", 10, 250, 50, step=10)

filtered = ranking.loc[
    ranking["recommended_product"].isin(product)
    & ranking["customer_segment"].isin(segment)
    & ranking["priority_rank"].le(max_rank)
].copy()

st.dataframe(filtered, use_container_width=True, hide_index=True)
