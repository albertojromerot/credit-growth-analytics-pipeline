from src.config import FEATURE_COLUMNS


def test_feature_list_has_no_target_like_columns():
    leakage_terms = ["target", "outcome", "converted_next", "responsible_credit_behaviour", "observed_product"]
    leakage_like = [col for col in FEATURE_COLUMNS if any(term in col.lower() for term in leakage_terms)]
    assert leakage_like == []
