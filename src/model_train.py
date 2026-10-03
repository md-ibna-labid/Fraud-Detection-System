# src/model_train.py

import pandas as pd
import numpy as np
import joblib
import sys
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

# Add src to path
sys.path.append(str(Path(__file__).parent))
from feature_engineering import engineer_features

def train_model():

    # ── Paths ──────────────────────────────────
    ROOT           = Path(__file__).parent.parent
    data_path      = ROOT / "data" / "synthetic_transactions.csv"
    processed_path = ROOT / "data" / "processed"
    models_path    = ROOT / "models"


    # ── Load data ──────────────────────────────
    df = pd.read_csv(data_path)
    df, feature_cols = engineer_features(df)

    X = df[feature_cols]
    y = df["is_anomaly"]

    # ── Split data ─────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2,
        stratify=y, random_state=42
    )

    test_df = df.loc[X_test.index].copy()
    test_df.to_csv(processed_path / "test_set.csv", index=False)
    print("✅ Test set saved")

    # ── Train Isolation Forest ─────────────────
    X_train_normal = X_train[y_train == 0]

    model = IsolationForest(
        n_estimators  = 200,
        contamination = 0.05,
        max_samples   = "auto",
        random_state  = 42,
        n_jobs        = -1
    )
    model.fit(X_train_normal)
    print("✅ Model trained on normal transactions")

    # ── Generate risk scores ───────────────────
    raw_scores  = model.decision_function(X_test)
    risk_scores = 100 * (
        1 - (raw_scores - raw_scores.min()) /
        (raw_scores.max() - raw_scores.min() + 1e-5)
    )

    test_df["risk_score"]        = risk_scores
    test_df["predicted_anomaly"] = (risk_scores >= 60).astype(int)
    test_df.to_csv(processed_path / "scored_transactions.csv", index=False)
    print("✅ Scored transactions saved")

    # ── Save model ─────────────────────────────
    joblib.dump({
        "model"       : model,
        "feature_cols": feature_cols
    }, models_path / "anomaly_model.pkl")

    print("✅ Model saved → models/anomaly_model.pkl")
    print(f"   Test samples : {len(X_test)}")
    print(f"   Flagged      : {test_df['predicted_anomaly'].sum()}")

    return model, feature_cols, test_df


if __name__ == "__main__":
    train_model()