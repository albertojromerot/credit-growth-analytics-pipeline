"""Governance monitoring page."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.title("Governance Monitoring")
checks_path = DATA_DIR / "governance_checks.csv"
ranking_path = DATA_DIR / "nba_ranked_customers.csv"

if not checks_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

checks = pd.read_csv(checks_path)
st.subheader("Pipeline governance checks")
st.dataframe(checks, use_container_width=True, hide_index=True)

if ranking_path.exists():
    ranking = pd.read_csv(ranking_path)
    exclusions = ranking["governance_exclusion_reason"].value_counts().reset_index()
    exclusions.columns = ["governance_exclusion_reason", "customers"]
    st.subheader("Governance exclusion distribution")
    st.dataframe(exclusions, use_container_width=True, hide_index=True)
