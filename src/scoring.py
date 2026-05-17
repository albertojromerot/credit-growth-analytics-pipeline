"""Score latest customers and generate a Next-Best-Action ranking."""
from __future__ import annotations

try:
    from src.config import (
        DASHBOARD_DATA_DIR,
        DATA_DIR,
        FEATURE_COLUMNS,
        MODEL_DIR,
        OUTPUT_DIR,
        TOP_N,
        ensure_project_directories,
    )
except ModuleNotFoundError:
    from config import (  # type: ignore
        DASHBOARD_DATA_DIR,
        DATA_DIR,
        FEATURE_COLUMNS,
        MODEL_DIR,
        OUTPUT_DIR,
        TOP_N,
        ensure_project_directories,
    )

import joblib
import numpy as np
import pandas as pd


def _select_recommended_product(row: pd.Series, products: pd.DataFrame) -> pd.Series:
    """Select a product using simple interpretable business rules."""
    eligible = products.loc[products["min_income_band_score"].le(row["income_band_score"])].copy()
    if eligible.empty:
        eligible = products.copy()

    if row["salary_inflow_flag"] == 1 and row["income_band_score"] >= 2:
        preferred = eligible.loc[eligible["product_id"].eq("P002")]
    elif row["income_band_score"] >= 3 and row["tenure_months"] >= 36:
        preferred = eligible.loc[eligible["product_id"].eq("P003")]
    elif row["age"] <= 35:
        preferred = eligible.loc[eligible["product_id"].eq("P004")]
    else:
        preferred = eligible.loc[eligible["product_id"].eq("P001")]

    if preferred.empty:
        preferred = eligible.sort_values("expected_value", ascending=False).head(1)
    return preferred.iloc[0]


def _reason_codes(row: pd.Series) -> str:
    """Create concise, adviser-readable reason codes."""
    reasons: list[str] = []
    if row["engagement_score"] >= 0.65:
        reasons.append("High recent engagement")
    if row["salary_inflow_flag"] == 1:
        reasons.append("Stable income signal")
    if row["recent_balance_growth"] > 0.08:
        reasons.append("Positive balance momentum")
    if row["utilisation_ratio"] <= 0.65:
        reasons.append("Controlled credit utilisation")
    if row["number_of_products"] >= 3:
        reasons.append("Established product relationship")
    if not reasons:
        reasons.append("Moderate profile; review manually")
    return " | ".join(reasons[:3])


def _recommended_action(row: pd.Series) -> str:
    if not row["eligible_for_responsible_offer"]:
        return "Do not contact - governance exclusion"
    if row["priority_rank"] <= 10:
        return "Priority adviser call with affordability review"
    if row["priority_rank"] <= TOP_N:
        return "Targeted credit-growth conversation"
    return "Nurture through low-intensity digital message"


def score_latest_customers() -> pd.DataFrame:
    """Generate the latest customer-level NBA ranking and dashboard-ready outputs."""
    ensure_project_directories()
    feature_path = OUTPUT_DIR / "feature_matrix.csv"
    if not feature_path.exists():
        raise FileNotFoundError("Missing outputs/feature_matrix.csv. Run src/features.py first.")

    conversion_model_path = MODEL_DIR / "conversion_model.joblib"
    responsible_model_path = MODEL_DIR / "responsible_behaviour_model.joblib"
    if not conversion_model_path.exists() or not responsible_model_path.exists():
        raise FileNotFoundError("Missing trained model artefacts. Run src/modelling.py first.")

    features = pd.read_csv(feature_path, parse_dates=["snapshot_month"])
    products = pd.read_csv(DATA_DIR / "credit_products.csv")
    latest_month = features["snapshot_month"].max()
    latest = features.loc[features["snapshot_month"].eq(latest_month)].copy()

    conversion_model = joblib.load(conversion_model_path)
    responsible_model = joblib.load(responsible_model_path)

    latest["p_conversion"] = conversion_model.predict_proba(latest[FEATURE_COLUMNS])[:, 1]
    latest["p_responsible"] = responsible_model.predict_proba(latest[FEATURE_COLUMNS])[:, 1]

    recommended_products = latest.apply(_select_recommended_product, axis=1, products=products)
    if not isinstance(recommended_products, pd.DataFrame):
        recommended_products = pd.DataFrame(recommended_products.tolist())
    recommended_products = recommended_products.reset_index(drop=True)
    latest = latest.reset_index(drop=True)

    latest["recommended_product_id"] = recommended_products["product_id"]
    latest["recommended_product"] = recommended_products["product_name"]
    latest["expected_credit_value"] = recommended_products["expected_value"].astype(float)

    latest["eligible_for_responsible_offer"] = (
        latest["arrears_last_6m"].eq(0)
        & latest["utilisation_ratio"].le(0.90)
        & latest["salary_inflow_flag"].eq(1)
        & latest["annual_income"].ge(18_000)
    )
    latest["governance_exclusion_reason"] = np.select(
        [
            latest["arrears_last_6m"].eq(1),
            latest["utilisation_ratio"].gt(0.90),
            latest["salary_inflow_flag"].eq(0),
            latest["annual_income"].lt(18_000),
        ],
        [
            "Recent arrears signal",
            "High utilisation",
            "No stable income signal",
            "Income below portfolio threshold",
        ],
        default="Eligible",
    )

    latest["responsible_nba_score"] = (
        latest["p_conversion"]
        * latest["p_responsible"]
        * latest["expected_credit_value"]
        * latest["eligible_for_responsible_offer"].astype(int)
    )
    latest = latest.sort_values("responsible_nba_score", ascending=False).reset_index(drop=True)
    latest["priority_rank"] = np.arange(1, len(latest) + 1)
    latest["reason_codes"] = latest.apply(_reason_codes, axis=1)
    latest["recommended_action"] = latest.apply(_recommended_action, axis=1)

    output_columns = [
        "customer_id",
        "snapshot_month",
        "priority_rank",
        "recommended_product_id",
        "recommended_product",
        "p_conversion",
        "p_responsible",
        "expected_credit_value",
        "responsible_nba_score",
        "eligible_for_responsible_offer",
        "governance_exclusion_reason",
        "reason_codes",
        "recommended_action",
        "region",
        "customer_segment",
        "income_band",
        "annual_income",
        "engagement_score",
        "utilisation_ratio",
        "arrears_last_6m",
    ]
    ranking = latest[output_columns].copy()
    ranking.to_csv(OUTPUT_DIR / "nba_ranked_customers.csv", index=False)
    ranking.to_csv(DASHBOARD_DATA_DIR / "nba_ranked_customers.csv", index=False)

    segment_summary = (
        ranking.head(TOP_N)
        .groupby(["customer_segment", "recommended_product"], dropna=False)
        .agg(
            customers=("customer_id", "count"),
            avg_score=("responsible_nba_score", "mean"),
            expected_value=("expected_credit_value", "sum"),
            avg_p_conversion=("p_conversion", "mean"),
            avg_p_responsible=("p_responsible", "mean"),
        )
        .reset_index()
        .sort_values("expected_value", ascending=False)
    )
    segment_summary.to_csv(OUTPUT_DIR / "segment_summary.csv", index=False)
    segment_summary.to_csv(DASHBOARD_DATA_DIR / "segment_summary.csv", index=False)
    return ranking


if __name__ == "__main__":
    scored = score_latest_customers()
    print(scored.head(TOP_N).to_string(index=False))
