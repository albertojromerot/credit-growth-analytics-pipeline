from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_generation import generate_all
from src.features import build_feature_matrix


def test_feature_matrix_has_unique_customer_month_keys():
    generate_all()
    df = build_feature_matrix()
    assert df.duplicated(["customer_id", "snapshot_month"]).sum() == 0


def test_feature_matrix_contains_targets():
    generate_all()
    df = build_feature_matrix()
    assert "converted_next_3m" in df.columns
    assert "responsible_credit_behaviour_6m" in df.columns
