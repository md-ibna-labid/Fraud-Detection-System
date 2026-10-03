# src/data_generator.py

import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

# ─────────────────────────────────────
# CONFIG
# ─────────────────────────────────────
NUM_USERS        = 500
NUM_TRANSACTIONS = 15000
ANOMALY_RATIO    = 0.05   # 5% anomalies

TRANSACTION_TYPES = [
    "send_money", "mobile_recharge",
    "bill_pay", "cash_out", "merchant_pay"
]

LOCATIONS = [
    "Dhaka", "Chittagong", "Sylhet",
    "Rajshahi", "Khulna", "Barishal"
]

DEVICES = ["android", "ios", "web"]


# ─────────────────────────────────────
# GENERATE NORMAL TRANSACTIONS
# ─────────────────────────────────────
def generate_normal_transactions(n):
    records = []
    for _ in range(n):
        user_id       = f"U{random.randint(1, NUM_USERS):04d}"
        amount        = round(np.random.lognormal(mean=6.5, sigma=0.8), 2)
        hour          = int(np.random.normal(loc=13, scale=3))
        hour          = max(7, min(22, hour))   # 7AM – 10PM normal
        location      = random.choice(LOCATIONS)
        device        = random.choice(DEVICES)
        txn_type      = random.choice(TRANSACTION_TYPES)
        recipient_new = random.random() < 0.10  # 10% new recipient
        records.append({
            "user_id"        : user_id,
            "amount"         : amount,
            "hour"           : hour,
            "location"       : location,
            "device"         : device,
            "txn_type"       : txn_type,
            "recipient_new"  : int(recipient_new),
            "is_anomaly"     : 0
        })
    return records


# ─────────────────────────────────────
# INJECT ANOMALY PATTERNS
# ─────────────────────────────────────
def generate_anomalies(n):
    records = []
    patterns = [
        "late_night_large",
        "new_device_large",
        "sudden_spike",
        "new_recipient_large",
        "unusual_location"
    ]
    for _ in range(n):
        user_id  = f"U{random.randint(1, NUM_USERS):04d}"
        pattern  = random.choice(patterns)

        if pattern == "late_night_large":
            amount       = round(random.uniform(8000, 25000), 2)
            hour         = random.choice([0, 1, 2, 3, 4])
            device       = random.choice(DEVICES)
            location     = random.choice(LOCATIONS)
            recipient_new = 0

        elif pattern == "new_device_large":
            amount        = round(random.uniform(5000, 20000), 2)
            hour          = random.randint(8, 21)
            device        = "web"   # sudden web login
            location      = random.choice(LOCATIONS)
            recipient_new = 0

        elif pattern == "sudden_spike":
            amount        = round(random.uniform(15000, 50000), 2)
            hour          = random.randint(8, 22)
            device        = random.choice(DEVICES)
            location      = random.choice(LOCATIONS)
            recipient_new = 0

        elif pattern == "new_recipient_large":
            amount        = round(random.uniform(7000, 30000), 2)
            hour          = random.randint(8, 22)
            device        = random.choice(DEVICES)
            location      = random.choice(LOCATIONS)
            recipient_new = 1   # always new recipient

        else:  # unusual_location
            amount        = round(random.uniform(3000, 15000), 2)
            hour          = random.randint(0, 5)
            device        = random.choice(DEVICES)
            location      = "Unknown"
            recipient_new = random.randint(0, 1)

        records.append({
            "user_id"        : user_id,
            "amount"         : amount,
            "hour"           : hour,
            "location"       : location,
            "device"         : device,
            "txn_type"       : random.choice(TRANSACTION_TYPES),
            "recipient_new"  : recipient_new,
            "is_anomaly"     : 1
        })
    return records


# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────
def generate_dataset():
    n_anomaly = int(NUM_TRANSACTIONS * ANOMALY_RATIO)
    n_normal  = NUM_TRANSACTIONS - n_anomaly

    normal    = generate_normal_transactions(n_normal)
    anomalies = generate_anomalies(n_anomaly)

    df = pd.DataFrame(normal + anomalies).sample(frac=1).reset_index(drop=True)
    df["txn_id"] = [f"TXN{i:06d}" for i in range(len(df))]

    df.to_csv("data/synthetic_transactions.csv", index=False)
    print(f"✅ Dataset saved: {len(df)} transactions")
    print(f"   Normal   : {n_normal}")
    print(f"   Anomalies: {n_anomaly}")
    return df


if __name__ == "__main__":
    generate_dataset()