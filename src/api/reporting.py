from src.api.llm.client import generate_investigation_report

def build_report(txn_summary: str, top_features: list, risk_score: float) -> dict:
    feature_names = [f["feature"] for f in top_features]
    return generate_investigation_report(txn_summary, feature_names, risk_score)