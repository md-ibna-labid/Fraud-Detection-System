from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

from src.api.scoring import score_single_transaction
from src.api.alerts import create_alert, get_all_alerts, update_alert_status
from src.api.reporting import build_report

app = FastAPI(
    title="Fraud Detection API",
    description="Phase 2 - Score transactions + AI investigation reports",
    version="1.0.0"
)

# 👇 CORS middleware eta exactly ekhane add kora (app er porei)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionInput(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    timestamp: str
    location: str
    device: str
    txn_type: str
    recipient_new: int = Field(0, ge=0, le=1)

class TransactionOutput(BaseModel):
    transaction_id: str
    risk_score: float
    is_suspicious: bool
    top_features: list
    report: dict

@app.get("/")
def root():
    return {"message": "Fraud Detection API is running"}

@app.post("/score", response_model=TransactionOutput)
def score_transaction(txn: TransactionInput):
    try:
        ts = datetime.fromisoformat(txn.timestamp)
        txn_dict = txn.model_dump()
        txn_dict["hour"] = ts.hour

        result = score_single_transaction(txn_dict)

        txn_summary = (
            f"User {txn.user_id} made a ${txn.amount:.2f} {txn.txn_type} "
            f"from {txn.location} using {txn.device} at {txn.timestamp}."
        )

        report = build_report(txn_summary, result["top_features"], result["risk_score"])

        if result["is_suspicious"]:
            create_alert(txn_dict, result["risk_score"], result["top_features"], report)

        return {
            "transaction_id": txn.transaction_id,
            "risk_score": result["risk_score"],
            "is_suspicious": result["is_suspicious"],
            "top_features": result["top_features"],
            "report": report
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
def list_alerts(status: str = None):
    return get_all_alerts(status)

@app.post("/alerts/{alert_id}/review")
def review_alert(alert_id: str):
    success = update_alert_status(alert_id, "reviewed")
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": f"Alert {alert_id} reviewed"}

@app.post("/alerts/{alert_id}/dismiss")
def dismiss_alert(alert_id: str):
    success = update_alert_status(alert_id, "dismissed")
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": f"Alert {alert_id} dismissed"}