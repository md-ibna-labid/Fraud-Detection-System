# src/model_evaluate.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
import sys
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

sys.path.append(str(Path(__file__).parent))
from feature_engineering import engineer_features

def evaluate_model():

    # ── Paths ──────────────────────────────────
    ROOT           = Path(__file__).parent.parent
    processed_path = ROOT / "data" / "processed"
    models_path    = ROOT / "models"

    # ── Load data ──────────────────────────────
    df       = pd.read_csv(processed_path / "scored_transactions.csv")
    artifact = joblib.load(models_path / "anomaly_model.pkl")

    model        = artifact["model"]
    feature_cols = artifact["feature_cols"]

    y_true = df["is_anomaly"]
    y_pred = df["predicted_anomaly"]

    # ── Metrics ────────────────────────────────
    print("=" * 45)
    print("        MODEL EVALUATION REPORT")
    print("=" * 45)
    print(classification_report(y_true, y_pred,
          target_names=["Normal", "Anomaly"]))

    auc = roc_auc_score(y_true, df["risk_score"] / 100)
    print(f"ROC-AUC Score : {auc:.4f}")

    # ── Confusion Matrix ───────────────────────
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d",
                xticklabels=["Normal","Anomaly"],
                yticklabels=["Normal","Anomaly"],
                cmap="Reds")
    plt.title("Confusion Matrix")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(processed_path / "confusion_matrix.png")
    print("✅ Confusion matrix saved")

    # ── Risk Score Distribution ────────────────
    plt.figure(figsize=(8, 4))
    df[df.is_anomaly == 0]["risk_score"].hist(
        bins=50, alpha=0.6, label="Normal", color="green")
    df[df.is_anomaly == 1]["risk_score"].hist(
        bins=50, alpha=0.6, label="Anomaly", color="red")
    plt.xlabel("Risk Score")
    plt.ylabel("Count")
    plt.title("Risk Score Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(processed_path / "risk_distribution.png")
    print("✅ Risk distribution saved")

    # ── SHAP Explainability ────────────────────
    X_test      = df[feature_cols]
    explainer   = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    plt.figure()
    shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(processed_path / "shap_summary.png")
    print("✅ SHAP summary saved")

    print("\n✅ Evaluation complete!")


if __name__ == "__main__":
    evaluate_model()