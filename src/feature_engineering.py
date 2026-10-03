# src/feature_engineering.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def engineer_features(df):

    df = df.copy()

    # ── Time features ──────────────────────────
    df["is_night"]    = (df["hour"] < 6).astype(int)
    df["is_off_hours"]= ((df["hour"] < 7) | (df["hour"] > 22)).astype(int)

    # ── Amount features ────────────────────────
    df["log_amount"]  = np.log1p(df["amount"])

    # ── User-level statistical baseline ────────
    user_stats = df.groupby("user_id")["amount"].agg(
        user_mean_amount = "mean",
        user_std_amount  = "std",
        user_max_amount  = "max"
    ).reset_index()
    df = df.merge(user_stats, on="user_id", how="left")
    df["user_std_amount"] = df["user_std_amount"].fillna(0)

    # Amount deviation from user baseline
    df["amount_deviation"] = (
        (df["amount"] - df["user_mean_amount"]) /
        (df["user_std_amount"] + 1e-5)
    )

    # ── Encode categoricals ────────────────────
    le = LabelEncoder()
    df["device_enc"]   = le.fit_transform(df["device"])
    df["location_enc"] = le.fit_transform(df["location"])
    df["txn_type_enc"] = le.fit_transform(df["txn_type"])

    # ── Final feature list ─────────────────────
    feature_cols = [
        "log_amount",
        "hour",
        "is_night",
        "is_off_hours",
        "recipient_new",
        "device_enc",
        "location_enc",
        "txn_type_enc",
        "user_mean_amount",
        "user_std_amount",
        "amount_deviation"
    ]

    print(f"✅ Features ready: {len(feature_cols)} features")
    return df, feature_cols


if __name__ == "__main__":
    df = pd.read_csv("data/synthetic_transactions.csv")
    df, features = engineer_features(df)
    df.to_csv("data/processed/featured_transactions.csv", index=False)
    print(df[features].head())