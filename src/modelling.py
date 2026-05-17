"""Train conversion and responsible-behaviour models for the NBA pipeline."""
from __future__ import annotations

try:
    from src.config import (
        CONVERSION_TARGET,
        DASHBOARD_DATA_DIR,
        DASHBOARD_DATA_DIR,
        MODEL_DIR,
        OUTPUT_DIR,
        RESPONSIBLE_TARGET,
        TOP_N,
        ensure_project_directories,
    )
    from src.preprocessing import build_preprocessor, get_feature_matrix_and_target, temporal_train_test_split
except ModuleNotFoundError:
    from config import (  # type: ignore
        CONVERSION_TARGET,
        DASHBOARD_DATA_DIR,
        DASHBOARD_DATA_DIR,
        MODEL_DIR,
        OUTPUT_DIR,
        RESPONSIBLE_TARGET,
        TOP_N,
        ensure_project_directories,
    )
    from preprocessing import build_preprocessor, get_feature_matrix_and_target, temporal_train_test_split  # type: ignore

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import average_precision_score, brier_score_loss, precision_score, roc_auc_score
from sklearn.pipeline import Pipeline


def _precision_at_k(y_true: pd.Series | np.ndarray, scores: np.ndarray, k: int = TOP_N) -> float:
    """Calculate precision among the top-k highest scores."""
    y = np.asarray(y_true).astype(int)
    k = min(k, len(y))
    if k == 0:
        return float("nan")
    order = np.argsort(scores)[::-1][:k]
    return float(y[order].mean())


def _safe_auc(y_true: pd.Series | np.ndarray, scores: np.ndarray) -> float:
    """Return ROC-AUC when both classes are present; otherwise return NaN."""
    y = np.asarray(y_true).astype(int)
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, scores))


def build_classifier(random_state: int = 42) -> Pipeline:
    """Create a reproducible model pipeline."""
    model = ExtraTreesClassifier(
        n_estimators=120,
        max_depth=9,
        min_samples_leaf=25,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )
    return Pipeline(steps=[("preprocessor", build_preprocessor()), ("model", model)])


def _fit_single_model(df: pd.DataFrame, target: str, model_name: str) -> tuple[Pipeline, dict[str, float]]:
    train, test = temporal_train_test_split(df, min_test_positives_col=target, test_months=3)
    x_train, y_train = get_feature_matrix_and_target(train, target)
    x_test, y_test = get_feature_matrix_and_target(test, target)

    pipeline = build_classifier()
    pipeline.fit(x_train, y_train)
    scores = pipeline.predict_proba(x_test)[:, 1]
    predictions = (scores >= 0.50).astype(int)

    metrics = {
        "model_name": model_name,
        "target": target,
        "train_rows": float(len(train)),
        "test_rows": float(len(test)),
        "train_positive_rate": float(y_train.mean()),
        "test_positive_rate": float(y_test.mean()),
        "roc_auc": _safe_auc(y_test, scores),
        "pr_auc": float(average_precision_score(y_test, scores)),
        "brier_score": float(brier_score_loss(y_test, scores)),
        "precision_at_50": _precision_at_k(y_test, scores, TOP_N),
        "precision_at_100": _precision_at_k(y_test, scores, 100),
        "classification_precision_threshold_050": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
    }
    joblib.dump(pipeline, MODEL_DIR / f"{model_name}.joblib")
    return pipeline, metrics


def train_models() -> pd.DataFrame:
    """Train both modelling components and save model KPIs."""
    ensure_project_directories()
    feature_path = OUTPUT_DIR / "feature_matrix.csv"
    if not feature_path.exists():
        raise FileNotFoundError("Missing outputs/feature_matrix.csv. Run src/features.py first.")

    df = pd.read_csv(feature_path, parse_dates=["snapshot_month"])
    _, conversion_metrics = _fit_single_model(df, CONVERSION_TARGET, "conversion_model")
    _, responsible_metrics = _fit_single_model(df, RESPONSIBLE_TARGET, "responsible_behaviour_model")

    metrics = pd.DataFrame([conversion_metrics, responsible_metrics])
    metrics.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)
    metrics.to_csv(DASHBOARD_DATA_DIR / "model_metrics.csv", index=False)

    validation_summary = metrics[[
        "model_name",
        "target",
        "roc_auc",
        "pr_auc",
        "brier_score",
        "precision_at_50",
        "precision_at_100",
    ]].copy()
    validation_summary.to_csv(OUTPUT_DIR / "validation_summary.csv", index=False)
    validation_summary.to_csv(DASHBOARD_DATA_DIR / "validation_summary.csv", index=False)
    return metrics


if __name__ == "__main__":
    trained_metrics = train_models()
    print(trained_metrics.to_string(index=False))
