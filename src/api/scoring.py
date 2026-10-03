import sys
import pandas as pd
import numpy as np
import joblib
import shap
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT / "src"))

from feature_engineering import engineer_features

MODEL_PATH = ROOT / "models" / "anomaly_model.pkl"

def load_model():
    artifact = joblib.load(MODEL_PATH)
    return artifact["model"], artifact["feature_cols"]

def score_single_transaction(txn_dict: dict) -> dict:
    df = pd.DataFrame([txn_dict])
    df_feat, feature_cols = engineer_features(df)

    model, _ = load_model()
    X = df_feat[feature_cols]

    raw_score = model.decision_function(X)[0]
    risk_score = 100 * (1 - (raw_score + 0.5) / 1.0)
    risk_score = max(0, min(100, risk_score))

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    abs_shap = np.abs(shap_values[0])
    top_indices = np.argsort(abs_shap)[-5:][::-1]

    top_features = [
        {"feature": feature_cols[i], "value": round(float(shap_values[0][i]), 4)}
        for i in top_indices
    ]

    return {
        "risk_score": round(risk_score, 2),
        "is_suspicious": bool(risk_score >= 60),
        "top_features": top_features
    }