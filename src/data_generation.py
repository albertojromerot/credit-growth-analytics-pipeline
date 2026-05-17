"""Generate synthetic customer, behaviour, product, outcome, and treatment-log data.

The generated data is fully synthetic and designed for a public portfolio project.
It must not be interpreted as real customer data or as a production credit policy.
"""
from __future__ import annotations

try:
    from src.config import (
        DATA_DIR,
        INCOME_BAND_ORDER,
        N_CUSTOMERS,
        N_MONTHS,
        PRODUCT_CATALOGUE,
        RANDOM_SEED,
        ensure_project_directories,
    )
except ModuleNotFoundError:  # Allows running as: python src/data_generation.py
    from config import (  # type: ignore
        DATA_DIR,
        INCOME_BAND_ORDER,
        N_CUSTOMERS,
        N_MONTHS,
        PRODUCT_CATALOGUE,
        RANDOM_SEED,
        ensure_project_directories,
    )

import numpy as np
import pandas as pd


def _sigmoid(x: np.ndarray | float) -> np.ndarray | float:
    return 1 / (1 + np.exp(-x))


def build_credit_products() -> pd.DataFrame:
    """Build a synthetic credit product catalogue with expected-value assumptions."""
    products = pd.DataFrame(PRODUCT_CATALOGUE)
    products["expected_gross_margin"] = (
        products["average_loan_amount"]
        * products["annual_margin_rate"]
        * (products["term_months"] / 12)
    )
    products["expected_funding_cost"] = (
        products["average_loan_amount"]
        * products["funding_cost_rate"]
        * (products["term_months"] / 12)
    )
    products["expected_operating_cost"] = products["average_loan_amount"] * products[
        "operating_cost_rate"
    ]
    products["expected_loss"] = products["average_loan_amount"] * products[
        "expected_loss_rate"
    ]
    products["expected_value"] = (
        products["expected_gross_margin"]
        - products["expected_funding_cost"]
        - products["expected_operating_cost"]
        - products["expected_loss"]
    ).round(2)
    return products


def build_customers(n_customers: int = N_CUSTOMERS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Create a customer-level synthetic table."""
    rng = np.random.default_rng(seed)

    income_bands = np.array(list(INCOME_BAND_ORDER.keys()))
    income_probs = np.array([0.16, 0.28, 0.31, 0.18, 0.07])
    selected_income_bands = rng.choice(income_bands, size=n_customers, p=income_probs)

    income_midpoints = {
        "Low": 18_000,
        "Lower-middle": 28_000,
        "Middle": 42_000,
        "Upper-middle": 62_000,
        "High": 95_000,
    }

    customers = pd.DataFrame(
        {
            "customer_id": [f"C{str(i).zfill(6)}" for i in range(1, n_customers + 1)],
            "age": np.clip(rng.normal(39, 12, n_customers).round(), 18, 74).astype(int),
            "income_band": selected_income_bands,
            "employment_type": rng.choice(
                ["Salaried", "Independent", "Contractor", "Pensioner"],
                size=n_customers,
                p=[0.58, 0.22, 0.13, 0.07],
            ),
            "region": rng.choice(
                [
                    "London",
                    "South East",
                    "Midlands",
                    "North West",
                    "South West",
                    "Scotland",
                    "Wales",
                ],
                size=n_customers,
                p=[0.34, 0.19, 0.15, 0.12, 0.10, 0.06, 0.04],
            ),
            "tenure_months": rng.integers(3, 180, n_customers),
            "digital_engagement_score": np.clip(rng.beta(2.2, 2.8, n_customers), 0, 1),
        }
    )
    customers["income_band_score"] = customers["income_band"].map(INCOME_BAND_ORDER).astype(int)
    income_noise = rng.normal(1.0, 0.16, n_customers)
    customers["annual_income"] = (
        customers["income_band"].map(income_midpoints).astype(float) * income_noise
    ).round(0)

    customers["customer_segment"] = np.select(
        [
            customers["tenure_months"] < 12,
            customers["digital_engagement_score"] >= 0.68,
            customers["income_band_score"] >= 4,
            customers["age"] >= 58,
        ],
        ["New customer", "Digital-first", "High-value", "Mature relationship"],
        default="Mass market",
    )
    return customers


def build_monthly_behaviour(customers: pd.DataFrame, n_months: int = N_MONTHS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Create customer-month behaviour signals."""
    rng = np.random.default_rng(seed + 1)
    months = pd.date_range("2024-01-31", periods=n_months, freq="ME")

    base = customers[[
        "customer_id",
        "annual_income",
        "income_band_score",
        "digital_engagement_score",
        "tenure_months",
    ]].copy()

    frames: list[pd.DataFrame] = []
    for month_idx, month in enumerate(months):
        monthly = base.copy()
        seasonality = 0.05 * np.sin((month_idx + 1) / 12 * 2 * np.pi)
        drift = month_idx / max(n_months - 1, 1)

        income_monthly = monthly["annual_income"] / 12
        savings_factor = rng.lognormal(mean=-0.65 + seasonality, sigma=0.55, size=len(monthly))
        credit_factor = rng.lognormal(mean=-1.35 + 0.15 * drift, sigma=0.75, size=len(monthly))

        monthly["snapshot_month"] = month
        monthly["savings_balance"] = (income_monthly * savings_factor).round(2)
        monthly["credit_balance"] = (income_monthly * credit_factor).round(2)
        monthly["number_of_products"] = np.clip(
            rng.poisson(1.2 + 0.35 * monthly["income_band_score"]), 1, 8
        )
        monthly["recent_balance_growth"] = np.clip(
            rng.normal(0.02 + 0.04 * monthly["digital_engagement_score"], 0.18, len(monthly)),
            -0.55,
            0.85,
        )
        monthly["recent_credit_enquiry_flag"] = rng.binomial(
            1,
            np.clip(0.08 + 0.11 * monthly["digital_engagement_score"], 0.02, 0.35),
            len(monthly),
        )
        monthly["salary_inflow_flag"] = rng.binomial(
            1,
            np.clip(0.58 + 0.07 * monthly["income_band_score"], 0.40, 0.95),
            len(monthly),
        )
        monthly["engagement_score"] = np.clip(
            0.55 * monthly["digital_engagement_score"]
            + 0.15 * monthly["recent_credit_enquiry_flag"]
            + rng.normal(0.08, 0.12, len(monthly)),
            0,
            1,
        )
        monthly["utilisation_ratio"] = np.clip(
            monthly["credit_balance"] / (monthly["annual_income"] / 3 + 1), 0, 1.35
        )
        arrears_probability = np.clip(
            0.04 + 0.22 * (monthly["utilisation_ratio"] > 0.85) - 0.025 * monthly["income_band_score"],
            0.01,
            0.35,
        )
        monthly["arrears_last_6m"] = rng.binomial(1, arrears_probability, len(monthly))
        frames.append(monthly.drop(columns=["annual_income", "income_band_score", "digital_engagement_score", "tenure_months"]))

    return pd.concat(frames, ignore_index=True)


def build_credit_outcomes(customers: pd.DataFrame, behaviour: pd.DataFrame, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Create synthetic conversion and responsible-behaviour labels."""
    rng = np.random.default_rng(seed + 2)
    base = behaviour.merge(
        customers[["customer_id", "income_band_score", "annual_income", "tenure_months", "customer_segment"]],
        on="customer_id",
        how="left",
    )

    conversion_logit = (
        -3.9
        + 1.9 * base["engagement_score"]
        + 0.65 * base["recent_credit_enquiry_flag"]
        + 0.30 * base["salary_inflow_flag"]
        + 0.10 * base["income_band_score"]
        + 0.45 * (base["recent_balance_growth"] > 0.08).astype(int)
        - 0.85 * base["arrears_last_6m"]
        - 0.35 * (base["utilisation_ratio"] > 0.95).astype(int)
    )
    p_conversion = np.clip(_sigmoid(conversion_logit), 0.005, 0.65)

    responsible_logit = (
        -0.25
        + 0.35 * base["income_band_score"]
        + 0.75 * base["salary_inflow_flag"]
        + 0.45 * (base["savings_balance"] > base["annual_income"] / 24).astype(int)
        - 1.55 * base["arrears_last_6m"]
        - 1.25 * (base["utilisation_ratio"] > 0.90).astype(int)
        - 0.20 * (base["tenure_months"] < 12).astype(int)
    )
    p_responsible = np.clip(_sigmoid(responsible_logit), 0.05, 0.97)

    products = build_credit_products()
    product_ids = products["product_id"].to_numpy()
    product_probabilities = np.array([0.32, 0.34, 0.18, 0.16])

    outcomes = base[["customer_id", "snapshot_month"]].copy()
    outcomes["converted_next_3m"] = rng.binomial(1, p_conversion)
    outcomes["responsible_credit_behaviour_6m"] = rng.binomial(1, p_responsible)
    outcomes["observed_product_id"] = np.where(
        outcomes["converted_next_3m"].eq(1),
        rng.choice(product_ids, size=len(outcomes), p=product_probabilities),
        "NONE",
    )
    outcomes["synthetic_p_conversion_true"] = np.round(p_conversion, 5)
    outcomes["synthetic_p_responsible_true"] = np.round(p_responsible, 5)
    return outcomes


def build_treatment_log_sample(customers: pd.DataFrame, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Create a sample treatment log to show the intended feedback loop."""
    rng = np.random.default_rng(seed + 3)
    sample = customers.sample(n=min(150, len(customers)), random_state=seed).copy()
    actions = [
        "A_AFFORDABILITY_REVIEW",
        "B_VALUE_AND_BENEFITS_MESSAGE",
        "C_DIGITAL_ONBOARDING_NUDGE",
        "CONTROL_NO_CONTACT",
    ]
    sample["recommendation_month"] = pd.Timestamp("2025-06-30")
    sample["recommended_action"] = rng.choice(actions, size=len(sample), p=[0.30, 0.32, 0.23, 0.15])
    sample["advisor_action"] = np.where(sample["recommended_action"].eq("CONTROL_NO_CONTACT"), "No contact", "Contacted")
    sample["contacted_flag"] = (sample["advisor_action"].eq("Contacted")).astype(int)
    sample["accepted_offer_flag"] = rng.binomial(1, np.where(sample["contacted_flag"].eq(1), 0.22, 0.05))
    sample["control_group_flag"] = sample["recommended_action"].eq("CONTROL_NO_CONTACT").astype(int)
    sample["outcome_1m"] = rng.choice(["accepted", "pending", "declined", "no_response"], size=len(sample), p=[0.16, 0.24, 0.25, 0.35])
    sample["outcome_3m"] = rng.choice(["converted", "not_converted", "excluded"], size=len(sample), p=[0.18, 0.72, 0.10])
    return sample[[
        "customer_id",
        "recommendation_month",
        "recommended_action",
        "advisor_action",
        "contacted_flag",
        "accepted_offer_flag",
        "control_group_flag",
        "outcome_1m",
        "outcome_3m",
    ]]


def generate_all() -> dict[str, pd.DataFrame]:
    """Generate all synthetic input tables and save them as CSV files."""
    ensure_project_directories()
    customers = build_customers()
    monthly_behaviour = build_monthly_behaviour(customers)
    credit_products = build_credit_products()
    credit_outcomes = build_credit_outcomes(customers, monthly_behaviour)
    treatment_log = build_treatment_log_sample(customers)

    tables = {
        "customers": customers,
        "monthly_behaviour": monthly_behaviour,
        "credit_products": credit_products,
        "credit_outcomes": credit_outcomes,
        "treatment_log_sample": treatment_log,
    }

    for name, table in tables.items():
        table.to_csv(DATA_DIR / f"{name}.csv", index=False)

    return tables


if __name__ == "__main__":
    generated = generate_all()
    for table_name, df in generated.items():
        print(f"Generated {table_name}: {df.shape[0]:,} rows x {df.shape[1]:,} columns")
