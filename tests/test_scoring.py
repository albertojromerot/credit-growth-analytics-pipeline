from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generation import generate_all
from src.features import build_feature_matrix
from src.modelling import train_models
from src.scoring import score_latest_customers


def test_scoring_creates_ranked_customer_list():
    generate_all()
    build_feature_matrix()
    train_models()
    ranking = score_latest_customers()
    assert ranking["priority_rank"].is_monotonic_increasing
    assert ranking["responsible_nba_score"].iloc[0] >= ranking["responsible_nba_score"].iloc[-1]
    assert {"p_conversion", "p_responsible", "expected_credit_value"}.issubset(ranking.columns)
