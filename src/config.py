"""Project configuration for the credit growth analytics pipeline."""
from __future__ import annotations

from pathlib import Path

RANDOM_SEED: int = 42
N_CUSTOMERS: int = 1_200
N_MONTHS: int = 18
TOP_N: int = 50

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "synthetic"
OUTPUT_DIR = ROOT_DIR / "outputs"
DASHBOARD_DATA_DIR = ROOT_DIR / "dashboard" / "data"
MODEL_DIR = OUTPUT_DIR / "models"

ID_COL = "customer_id"
TIME_COL = "snapshot_month"
CONVERSION_TARGET = "converted_next_3m"
RESPONSIBLE_TARGET = "responsible_credit_behaviour_6m"

INCOME_BAND_ORDER = {
    "Low": 1,
    "Lower-middle": 2,
    "Middle": 3,
    "Upper-middle": 4,
    "High": 5,
}

PRODUCT_CATALOGUE = [
    {
        "product_id": "P001",
        "product_name": "Responsible Personal Loan",
        "average_loan_amount": 7_500,
        "term_months": 30,
        "annual_margin_rate": 0.105,
        "funding_cost_rate": 0.048,
        "operating_cost_rate": 0.018,
        "expected_loss_rate": 0.028,
        "min_income_band_score": 2,
    },
    {
        "product_id": "P002",
        "product_name": "Payroll-linked Credit",
        "average_loan_amount": 10_000,
        "term_months": 36,
        "annual_margin_rate": 0.095,
        "funding_cost_rate": 0.044,
        "operating_cost_rate": 0.014,
        "expected_loss_rate": 0.020,
        "min_income_band_score": 2,
    },
    {
        "product_id": "P003",
        "product_name": "Green Home Improvement Loan",
        "average_loan_amount": 15_000,
        "term_months": 48,
        "annual_margin_rate": 0.090,
        "funding_cost_rate": 0.045,
        "operating_cost_rate": 0.016,
        "expected_loss_rate": 0.024,
        "min_income_band_score": 3,
    },
    {
        "product_id": "P004",
        "product_name": "Education Credit Line",
        "average_loan_amount": 5_000,
        "term_months": 24,
        "annual_margin_rate": 0.085,
        "funding_cost_rate": 0.043,
        "operating_cost_rate": 0.017,
        "expected_loss_rate": 0.018,
        "min_income_band_score": 1,
    },
]

FEATURE_COLUMNS = [
    "age",
    "tenure_months",
    "annual_income",
    "income_band_score",
    "digital_engagement_score",
    "savings_balance",
    "credit_balance",
    "number_of_products",
    "recent_balance_growth",
    "recent_credit_enquiry_flag",
    "salary_inflow_flag",
    "engagement_score",
    "utilisation_ratio",
    "arrears_last_6m",
    "balance_to_income_ratio",
    "credit_to_income_ratio",
    "product_depth_score",
    "affordability_proxy",
    "region",
    "employment_type",
    "customer_segment",
]

CATEGORICAL_FEATURES = ["region", "employment_type", "customer_segment"]
NUMERIC_FEATURES = [c for c in FEATURE_COLUMNS if c not in CATEGORICAL_FEATURES]


def ensure_project_directories() -> None:
    """Create expected output folders if they do not exist."""
    for path in [DATA_DIR, OUTPUT_DIR, DASHBOARD_DATA_DIR, MODEL_DIR]:
        path.mkdir(parents=True, exist_ok=True)
