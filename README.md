# 🛡️ Fraud Detection System — Real-Time Fraud Detection & Investigation Dashboard

*An end-to-end ML & AI-powered real-time fraud detection dashboard for financial transactions.*

## 📌 Overview

Fraud Detection System is a complete fraud detection and investigation system that simulates how financial institutions monitor, investigate, and respond to suspicious transactions in real time.

**Workflow:** Transaction Generation → Feature Engineering → Anomaly Detection → Risk Scoring → Alert Generation → Investigation Report → Dashboard Visualization

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | FastAPI, Python 3.10+, Uvicorn |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, Lucide Icons |
| **ML Model** | Isolation Forest (Scikit-learn) + Rule-based hybrid |
| **AI/LLM** | Ollama — Llama 3.2 (for investigation report generation) |
| **Data** | Pandas, NumPy, SHAP, Matplotlib, Faker |
| **Storage** | In-memory (Python dictionaries) |
| **DevOps** | Git, GitHub, Vercel (Frontend), Render (Backend) |

## ✨ Key Features

- Real-time transaction scoring (0–100 risk score per transaction)
- ML anomaly detection — Isolation Forest + Rule-based hybrid algorithm
- LLM-generated risk reports — What happened / Why risky / Recommended action
- Interactive Admin Dashboard built with Next.js
- Alert Review/Dismiss workflow for full alert management
- SHAP explainability for feature importance analysis
- Live feed simulation for real-time transaction monitoring

## ⚙️ Setup & Installation

### Prerequisites

| Tool | Version |
| --- | --- |
| Python | 3.10+ |
| Node.js | 18+ |
| npm | Latest |
| Git | Latest |

### Step 1: Clone Repository

```bash
git clone https://github.com/md-ibna-labid/fraud-detection-system.git
cd fraud-detection-system
cd fraud-detection
```

### Step 2: Backend Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

### Step 3: Ollama Setup (for LLM reports)

```bash
ollama pull llama3.2
ollama run llama3.2
```

### Step 4: Frontend Setup

```bash
cd dashboard
npm install
npm run dev
```

Now open:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📁 Project Structure

```
fraud-detection/
│
├── dashboard/                         # Frontend (Next.js)
│
├── data/
│   ├── processed/                     # Evaluation artifacts
│   │   ├── alerts.json
│   │   ├── confusion_matrix.png
│   │   ├── risk_distribution.png
│   │   ├── scored_transactions.csv
│   │   ├── shap_summary.png
│   │   └── test_set.csv
│   └── raw/
│       └── synthetic_transactions.csv
│
├── models/
│   └── anomaly_model.pkl              # Trained ML model
│
├── notebooks/
│   └── exploration.ipynb
│
├── src/
│   ├── api/                           # FastAPI backend
│   │   ├── alerts.py                  # Alert generation / retrieval logic
│   │   ├── main.py                    # Entry point
│   │   ├── reporting.py               # Investigation report generation (LLM)
│   │   └── scoring.py                 # Risk scoring engine
│   ├── data_generator.py              # Synthetic data creator
│   ├── feature_engineering.py         # Feature extraction
│   ├── model_evaluate.py              # Model evaluation
│   └── model_train.py                 # Model training pipeline
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Folder Descriptions

| Folder | Purpose |
| --- | --- |
| `dashboard/` | Next.js frontend — all UI code |
| `data/processed/` | Evaluation outputs (charts, scored data, alerts) |
| `models/` | Trained ML model artifact |
| `notebooks/` | Jupyter notebook for exploration |
| `src/api/` | FastAPI backend — all API logic |
| `src/` | ML pipeline (data gen, training, evaluation) |

## 📡 API Endpoints

### 1. `POST /api/analyze-transactions`

Scores all transactions and generates investigation reports.

**Response:**

```json
{
  "transactions": [
    {
      "id": "TXN_001",
      "customer_name": "Rafiq Hassan",
      "amount": 25000,
      "type": "transfer",
      "location": "Dhaka",
      "risk_score": 72.5,
      "risk_level": "High",
      "reasons": [
        "Amount 12x higher than average",
        "Transaction at 2:30 AM",
        "New recipient added today"
      ],
      "investigation_report": {
        "what_happened": "A transfer of BDT 25,000 was initiated to a new recipient at 2:30 AM from Dhaka.",
        "why_risky": "Amount significantly higher than normal. Time is outside regular activity hours. Recipient has no transaction history.",
        "recommended_action": "Temporarily block the transaction. Contact the customer via phone. If unresponsive, escalate for manual review."
      }
    }
  ],
  "summary": {
    "total": 20,
    "high_risk": 3,
    "medium_risk": 4,
    "low_risk": 13
  }
}
```

### 2. `GET /alerts`

Returns a list of all generated alerts (automatically created from high-risk transactions).

### 3. `POST /alerts/{id}/review`

Marks a specific alert as reviewed.

### 4. `POST /alerts/{id}/dismiss`

Dismisses a specific alert.

## 🧠 Detection Approach

**Hybrid Strategy:** Isolation Forest (60%) + Rule-based checks (40%)

**Risk Score Formula:**

```
Risk Score = (Anomaly Score × 0.6) + (Rule Score × 0.4)
```

**Features Used:** `amount_ratio`, `hour_of_day`, `is_new_recipient`, `is_new_device`, `is_new_location`, `txn_frequency`, `amount_zscore`

## 📊 Evaluation Artifacts (`data/processed/`)

| File | Description |
| --- | --- |
| `confusion_matrix.png` | Model performance |
| `risk_distribution.png` | Score distribution |
| `shap_summary.png` | Feature importance |
| `scored_transactions.csv` | All transactions scored |
| `alerts.json` | Generated alerts |

## 🎮 Demo Instructions

1. Open http://localhost:3000
2. Click **Run Demo Scenario**
3. Watch transactions appear gradually (Low → Medium → High risk)
4. Click any high-risk transaction to view its investigation report

### Demo Risk Distribution

| Risk Level | Count |
| --- | --- |
| Low | 13 |
| Medium | 4 |
| High | 3 |
| **Total** | **20** |

## 🌐 Deployment

### Backend → Render

- **Root:** `src/api`
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend → Vercel

- **Root:** `dashboard`
- **Framework:** Next.js
- **Env:** `NEXT_PUBLIC_API_URL`

## 👥 Team Members

- Shihab Ar Rafi
- Raiyan Jahan
- Md. Ibna Labid


-

**Fraud Detection System** — Detecting suspicious transactions with intelligence, explainability, and action-ready reporting.