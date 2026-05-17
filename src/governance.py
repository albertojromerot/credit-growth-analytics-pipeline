"""Governance checks for the portfolio pipeline."""
from __future__ import annotations

try:
    from src.config import DASHBOARD_DATA_DIR, DATA_DIR, FEATURE_COLUMNS, OUTPUT_DIR, TIME_COL, ensure_project_directories
except ModuleNotFoundError:
    from config import DASHBOARD_DATA_DIR, DATA_DIR, FEATURE_COLUMNS, OUTPUT_DIR, TIME_COL, ensure_project_directories  # type: ignore

import pandas as pd


LEAKAGE_TERMS = ["target", "outcome", "converted_next", "responsible_credit_behaviour", "observed_product"]


def run_governance_checks() -> pd.DataFrame:
    """Run data, leakage, and ranking governance checks."""
    ensure_project_directories()
    feature_path = OUTPUT_DIR / "feature_matrix.csv"
    ranking_path = OUTPUT_DIR / "nba_ranked_customers.csv"

    if not feature_path.exists():
        raise FileNotFoundError("Missing outputs/feature_matrix.csv. Run src/features.py first.")

    features = pd.read_csv(feature_path, parse_dates=[TIME_COL])
    checks: list[dict[str, object]] = []

    duplicated_keys = features.duplicated(["customer_id", TIME_COL]).sum()
    checks.append({
        "check_name": "unique_customer_month_key",
        "status": "pass" if duplicated_keys == 0 else "fail",
        "value": int(duplicated_keys),
        "notes": "Duplicated customer-month rows in feature matrix.",
    })

    missing_feature_columns = [col for col in FEATURE_COLUMNS if col not in features.columns]
    checks.append({
        "check_name": "expected_feature_columns_present",
        "status": "pass" if not missing_feature_columns else "fail",
        "value": len(missing_feature_columns),
        "notes": ", ".join(missing_feature_columns) if missing_feature_columns else "All expected features present.",
    })

    leakage_like_features = [
        col for col in FEATURE_COLUMNS if any(term in col.lower() for term in LEAKAGE_TERMS)
    ]
    checks.append({
        "check_name": "feature_name_leakage_scan",
        "status": "pass" if not leakage_like_features else "review",
        "value": len(leakage_like_features),
        "notes": ", ".join(leakage_like_features) if leakage_like_features else "No leakage-like feature names detected.",
    })

    missingness = features[FEATURE_COLUMNS].isna().mean().sort_values(ascending=False)
    high_missing = missingness[missingness > 0.30]
    checks.append({
        "check_name": "high_missingness_features",
        "status": "pass" if high_missing.empty else "review",
        "value": int(len(high_missing)),
        "notes": high_missing.round(3).to_dict() if not high_missing.empty else "No feature has missingness above 30%.",
    })

    if ranking_path.exists():
        ranking = pd.read_csv(ranking_path, parse_dates=[TIME_COL])
        top_50 = ranking.nsmallest(50, "priority_rank")
        excluded_top_50 = (~top_50["eligible_for_responsible_offer"].astype(bool)).sum()
        checks.append({
            "check_name": "top_50_governance_exclusions",
            "status": "pass" if excluded_top_50 == 0 else "fail",
            "value": int(excluded_top_50),
            "notes": "Number of Top 50 records excluded by responsible-lending guardrails.",
        })
    else:
        checks.append({
            "check_name": "ranking_file_present",
            "status": "review",
            "value": 0,
            "notes": "Ranking file not found yet; run src/scoring.py.",
        })

    products_path = DATA_DIR / "credit_products.csv"
    checks.append({
        "check_name": "synthetic_product_catalogue_present",
        "status": "pass" if products_path.exists() else "fail",
        "value": int(products_path.exists()),
        "notes": "Synthetic expected-value product assumptions file.",
    })

    results = pd.DataFrame(checks)
    results.to_csv(OUTPUT_DIR / "governance_checks.csv", index=False)
    results.to_csv(DASHBOARD_DATA_DIR / "governance_checks.csv", index=False)
    return results


if __name__ == "__main__":
    governance = run_governance_checks()
    print(governance.to_string(index=False))
