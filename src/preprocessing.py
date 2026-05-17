"""Preprocessing helpers for temporal modelling and validation."""
from __future__ import annotations

try:
    from src.config import CATEGORICAL_FEATURES, FEATURE_COLUMNS, NUMERIC_FEATURES, TIME_COL
except ModuleNotFoundError:  # Allows importing from scripts executed inside src/
    from config import CATEGORICAL_FEATURES, FEATURE_COLUMNS, NUMERIC_FEATURES, TIME_COL  # type: ignore

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def make_onehot_encoder() -> OneHotEncoder:
    """Create a version-safe dense one-hot encoder."""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:  # pragma: no cover - compatibility for older sklearn versions
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_preprocessor() -> ColumnTransformer:
    """Build the modelling preprocessor for numeric and categorical features."""
    numeric_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_onehot_encoder()),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def temporal_train_test_split(
    df: pd.DataFrame,
    min_test_positives_col: str,
    test_months: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create a simple time-ordered train/test split.

    The test set uses the latest months with at least one positive label for the selected target.
    This prevents an uninformative test month when the target has no positives.
    """
    work = df.copy()
    work[TIME_COL] = pd.to_datetime(work[TIME_COL])
    months = sorted(work[TIME_COL].dropna().unique())

    candidate_months = []
    for month in reversed(months):
        month_slice = work.loc[work[TIME_COL].eq(month)]
        if month_slice[min_test_positives_col].sum() > 0:
            candidate_months.append(month)
        if len(candidate_months) >= test_months:
            break

    if not candidate_months:
        raise ValueError(f"No positive labels found for target {min_test_positives_col!r}.")

    test_month_set = set(candidate_months)
    train = work.loc[~work[TIME_COL].isin(test_month_set)].copy()
    test = work.loc[work[TIME_COL].isin(test_month_set)].copy()

    if train.empty or test.empty:
        raise ValueError("Temporal split produced an empty train or test set.")

    return train, test


def get_feature_matrix_and_target(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    """Return feature matrix and target vector using the governed feature list."""
    missing_features = [feature for feature in FEATURE_COLUMNS if feature not in df.columns]
    if missing_features:
        raise ValueError(f"Missing expected features: {missing_features}")
    if target not in df.columns:
        raise ValueError(f"Missing target column: {target}")
    return df[FEATURE_COLUMNS].copy(), df[target].astype(int).copy()
