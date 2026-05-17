"""Run the full reproducible portfolio pipeline end to end."""
from __future__ import annotations

try:
    from src.data_generation import generate_all
    from src.features import build_feature_matrix
    from src.governance import run_governance_checks
    from src.modelling import train_models
    from src.scoring import score_latest_customers
    from src.validation import build_benchmark_comparison
except ModuleNotFoundError:
    from data_generation import generate_all  # type: ignore
    from features import build_feature_matrix  # type: ignore
    from governance import run_governance_checks  # type: ignore
    from modelling import train_models  # type: ignore
    from scoring import score_latest_customers  # type: ignore
    from validation import build_benchmark_comparison  # type: ignore


def main() -> None:
    """Execute all pipeline stages."""
    print("[01] Generating synthetic data")
    generate_all()

    print("[02] Building feature matrix")
    build_feature_matrix()

    print("[03] Training models")
    metrics = train_models()
    print(metrics.to_string(index=False))

    print("[04] Scoring latest customers")
    ranking = score_latest_customers()
    print(ranking.head(10).to_string(index=False))

    print("[05] Building validation benchmark")
    comparison = build_benchmark_comparison()
    print(comparison.to_string(index=False))

    print("[06] Running governance checks")
    checks = run_governance_checks()
    print(checks.to_string(index=False))

    print("Pipeline completed. Check the outputs/ and dashboard/data/ folders.")


if __name__ == "__main__":
    main()
