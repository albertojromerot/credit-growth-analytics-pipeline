"""Governance monitoring page for the portfolio dashboard."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

st.set_page_config(page_title="Governance Monitoring", layout="wide")
st.title("Governance Monitoring")
st.caption("Data-quality checks, responsible-lending exclusions, and audit signals.")

checks_path = DATA_DIR / "governance_checks.csv"
ranking_path = DATA_DIR / "nba_ranked_customers.csv"

if not checks_path.exists():
    st.warning("Run `python -m src.run_pipeline` first.")
    st.stop()

checks = pd.read_csv(checks_path)
ranking = pd.read_csv(ranking_path) if ranking_path.exists() else pd.DataFrame()

st.markdown(
    """
This page makes the governance layer visible. The model is positioned as a decision-support tool, not an automated credit approval system.
The checks below help a reviewer understand whether the pipeline is auditable, reproducible, and aligned with responsible targeting.
"""
)

passed = int(checks["status"].eq("pass").sum())
failed = int(checks["status"].ne("pass").sum())
col1, col2, col3 = st.columns(3)
col1.metric("Checks passed", passed)
col2.metric("Checks requiring review", failed)
col3.metric("Total checks", len(checks))

st.subheader("Pipeline governance checks")
st.dataframe(checks, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Check status distribution")
    status_counts = checks["status"].value_counts().reset_index()
    status_counts.columns = ["status", "checks"]
    st.plotly_chart(px.bar(status_counts, x="status", y="checks", text="checks"), use_container_width=True)

with right:
    st.subheader("Governance checks by value")
    fig_checks = px.bar(checks, x="check_name", y="value", color="status", title="Audit-check values")
    fig_checks.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_checks, use_container_width=True)

if not ranking.empty:
    st.divider()
    st.subheader("Responsible-lending exclusion distribution")
    exclusions = ranking["governance_exclusion_reason"].value_counts().reset_index()
    exclusions.columns = ["governance_exclusion_reason", "customers"]
    st.plotly_chart(
        px.bar(
            exclusions,
            x="customers",
            y="governance_exclusion_reason",
            orientation="h",
            text="customers",
            title="Customers by governance status or exclusion reason",
        ),
        use_container_width=True,
    )

    top_50 = ranking.nsmallest(50, "priority_rank")
    st.subheader("Top 50 governance review")
    st.dataframe(
        top_50[[
            "priority_rank",
            "customer_id",
            "eligible_for_responsible_offer",
            "governance_exclusion_reason",
            "recommended_action",
            "reason_codes",
        ]],
        use_container_width=True,
        hide_index=True,
    )

st.info(
    "In a real institution, this layer would be extended with compliance review, affordability policy, fairness checks, consent controls, and post-intervention monitoring."
)
