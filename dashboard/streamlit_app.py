"""Main dashboard landing page for the Credit Growth Analytics Pipeline."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"
TOP_N = 50

st.set_page_config(
    page_title="Credit Growth Analytics Pipeline",
    page_icon="📊",
    layout="wide",
)


def _load_csv(path: Path, **kwargs) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, **kwargs)


def _fmt_currency(value: float) -> str:
    return f"£{value:,.0f}"


def _fmt_pct(value: float) -> str:
    return f"{value:.1%}"


ranking_path = DATA_DIR / "nba_ranked_customers.csv"
metrics_path = DATA_DIR / "model_metrics.csv"
benchmark_path = DATA_DIR / "benchmark_comparison.csv"
checks_path = DATA_DIR / "governance_checks.csv"

st.title("Credit Growth Analytics Pipeline")
st.caption("Responsible Customer Lifetime Value / Next-Best-Action Model")

st.markdown(
    """
This dashboard is the portfolio equivalent of a Power BI decision layer. It translates the model output into an
executive view of credit-growth opportunity, customer ranking, model performance, and governance controls.

The key question is not only **who is likely to accept a credit offer**, but who is likely to convert, behave
responsibly, and generate sustainable expected value after eligibility rules are applied.
"""
)

if not ranking_path.exists():
    st.warning(
        "Dashboard data has not been generated yet. Run `python -m src.run_pipeline` "
        "from the repository root, then refresh this dashboard."
    )
    st.stop()

ranking = _load_csv(ranking_path, parse_dates=["snapshot_month"])
metrics = _load_csv(metrics_path)
benchmark = _load_csv(benchmark_path)
checks = _load_csv(checks_path)

top_50 = ranking.nsmallest(TOP_N, "priority_rank")
latest_snapshot = ranking["snapshot_month"].max().date()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Latest snapshot", str(latest_snapshot))
col2.metric("Customers scored", f"{len(ranking):,}")
col3.metric("Top 50 expected value", _fmt_currency(top_50["expected_credit_value"].sum()))
col4.metric("Top 50 avg. conversion", _fmt_pct(top_50["p_conversion"].mean()))
col5.metric("Top 50 eligible share", _fmt_pct(top_50["eligible_for_responsible_offer"].astype(bool).mean()))

st.divider()

left, right = st.columns([1.15, 0.85])

with left:
    st.subheader("Executive interpretation")
    st.markdown(
        f"""
- **Decision objective:** prioritise the best customers for responsible credit-growth conversations.
- **Current action pool:** the Top {TOP_N} list represents the highest-priority customers after model scoring and governance filters.
- **Commercial proxy:** the Top {TOP_N} customers represent **{_fmt_currency(top_50['expected_credit_value'].sum())}** in expected credit value.
- **Governance signal:** **{_fmt_pct(top_50['eligible_for_responsible_offer'].astype(bool).mean())}** of the Top {TOP_N} are eligible under the current responsible-lending guardrails.
"""
    )

    st.subheader("Top 10 priority recommendations")
    st.dataframe(
        top_50.head(10)[[
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
        column_config={
            "p_conversion": st.column_config.ProgressColumn("p_conversion", format="%.1f", min_value=0, max_value=1),
            "p_responsible": st.column_config.ProgressColumn("p_responsible", format="%.1f", min_value=0, max_value=1),
            "expected_credit_value": st.column_config.NumberColumn("expected_credit_value", format="£%.0f"),
            "responsible_nba_score": st.column_config.NumberColumn("responsible_nba_score", format="%.1f"),
        },
    )

with right:
    st.subheader("Top 50 product mix")
    product_mix = top_50.groupby("recommended_product", as_index=False).size()
    fig_product = px.pie(
        product_mix,
        names="recommended_product",
        values="size",
        hole=0.45,
        title="Recommended products",
    )
    st.plotly_chart(fig_product, use_container_width=True)

    st.subheader("Priority-score distribution")
    fig_score = px.histogram(
        ranking.head(250),
        x="responsible_nba_score",
        nbins=30,
        title="Top 250 responsible NBA scores",
    )
    st.plotly_chart(fig_score, use_container_width=True)

if not benchmark.empty:
    st.divider()
    st.subheader("Benchmark comparison")
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
        title="Rule-based vs model-based targeting",
    )
    fig_benchmark.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_benchmark, use_container_width=True)

if not metrics.empty or not checks.empty:
    st.divider()
    metric_col, governance_col = st.columns(2)
    with metric_col:
        st.subheader("Model KPI snapshot")
        display_metrics = metrics[[
            "model_name",
            "roc_auc",
            "pr_auc",
            "brier_score",
            "precision_at_50",
        ]].copy()
        st.dataframe(display_metrics, use_container_width=True, hide_index=True)
    with governance_col:
        st.subheader("Governance check status")
        status_counts = checks["status"].value_counts().reset_index() if not checks.empty else pd.DataFrame()
        if not status_counts.empty:
            status_counts.columns = ["status", "checks"]
            st.dataframe(status_counts, use_container_width=True, hide_index=True)
        st.info("Navigate to the pages in the sidebar for customer ranking, model performance, and governance monitoring.")
