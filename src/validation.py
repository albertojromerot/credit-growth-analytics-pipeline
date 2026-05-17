"""Create benchmark and validation summaries for the NBA pipeline."""
from __future__ import annotations

try:
    from src.config import DASHBOARD_DATA_DIR, OUTPUT_DIR, TOP_N, ensure_project_directories
except ModuleNotFoundError:
    from config import DASHBOARD_DATA_DIR, OUTPUT_DIR, TOP_N, ensure_project_directories  # type: ignore

import pandas as pd


def build_benchmark_comparison() -> pd.DataFrame:
    """Compare simple rule-based targeting with model-driven ranking.

    The comparison is intentionally transparent for a portfolio repository. It uses the
    latest labelled feature matrix and compares a manual score against the NBA score.
    """
    ensure_project_directories()
    feature_path = OUTPUT_DIR / "feature_matrix.csv"
    ranking_path = OUTPUT_DIR / "nba_ranked_customers.csv"
    if not feature_path.exists() or not ranking_path.exists():
        raise FileNotFoundError("Run feature engineering and scoring before validation.")

    features = pd.read_csv(feature_path, parse_dates=["snapshot_month"])
    ranking = pd.read_csv(ranking_path, parse_dates=["snapshot_month"])
    latest_month = features["snapshot_month"].max()
    latest_labels = features.loc[features["snapshot_month"].eq(latest_month), [
        "customer_id",
        "converted_next_3m",
        "responsible_credit_behaviour_6m",
        "income_band_score",
        "salary_inflow_flag",
    ]].copy()

    eval_df = ranking.merge(latest_labels, on="customer_id", how="left", validate="one_to_one")
    eval_df["manual_rule_score"] = (
        eval_df["income_band_score"]
        + 2 * eval_df["engagement_score"]
        + eval_df["salary_inflow_flag"]
        - 2 * eval_df["arrears_last_6m"]
        - eval_df["utilisation_ratio"]
    )
    eval_df["conversion_only_score"] = eval_df["p_conversion"]
    eval_df["responsible_nba_score"] = eval_df["responsible_nba_score"]
    eval_df["responsible_conversion"] = (
        eval_df["converted_next_3m"].fillna(0).astype(int)
        * eval_df["responsible_credit_behaviour_6m"].fillna(0).astype(int)
    )

    rows = []
    for approach, score_col in [
        ("Manual rule-based segmentation", "manual_rule_score"),
        ("Conversion-only model", "conversion_only_score"),
        ("Responsible NBA model", "responsible_nba_score"),
    ]:
        top = eval_df.sort_values(score_col, ascending=False).head(TOP_N)
        rows.append({
            "approach": approach,
            "top_n": TOP_N,
            "precision_at_50_conversion": float(top["converted_next_3m"].mean()),
            "precision_at_50_responsible_conversion": float(top["responsible_conversion"].mean()),
            "expected_value_captured": float(top["expected_credit_value"].sum()),
            "eligible_share": float(top["eligible_for_responsible_offer"].astype(bool).mean()),
        })

    comparison = pd.DataFrame(rows)
    comparison.to_csv(OUTPUT_DIR / "benchmark_comparison.csv", index=False)
    comparison.to_csv(DASHBOARD_DATA_DIR / "benchmark_comparison.csv", index=False)
    return comparison


if __name__ == "__main__":
    comparison_df = build_benchmark_comparison()
    print(comparison_df.to_string(index=False))
