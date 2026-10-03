import json
import uuid
from datetime import datetime
from pathlib import Path

ALERTS_PATH = Path(__file__).parent.parent.parent / "data" / "processed" / "alerts.json"

def _load_alerts():
    if ALERTS_PATH.exists():
        with open(ALERTS_PATH, "r") as f:
            return json.load(f)
    return []

def _save_alerts(alerts):
    ALERTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_PATH, "w") as f:
        json.dump(alerts, f, indent=2)

def create_alert(txn_data: dict, risk_score: float, top_features: list, report: dict) -> dict:
    alerts = _load_alerts()
    alert = {
        "alert_id": str(uuid.uuid4())[:8],
        "transaction_id": txn_data.get("transaction_id", "unknown"),
        "user_id": txn_data.get("user_id", "unknown"),
        "amount": txn_data.get("amount", 0),
        "risk_score": risk_score,
        "status": "flagged",
        "top_features": top_features,
        "report": report,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    alerts.append(alert)
    _save_alerts(alerts)
    return alert

def get_all_alerts(status: str = None):
    alerts = _load_alerts()
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    return sorted(alerts, key=lambda x: x["created_at"], reverse=True)

def update_alert_status(alert_id: str, new_status: str) -> bool:
    alerts = _load_alerts()
    for alert in alerts:
        if alert["alert_id"] == alert_id:
            alert["status"] = new_status
            alert["updated_at"] = datetime.now().isoformat()
            _save_alerts(alerts)
            return True
    return False