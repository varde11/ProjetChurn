# 📉 Churn Decision Intelligence App

> A deployed machine learning application that goes beyond churn prediction by integrating business strategy and ROI optimization.

**🔗 [Live Demo](https://varde11-churn-frontend.hf.space/)**

---

## 🚀 Project Overview

Most churn projects stop at classification. But **predicting churn is not enough.**

This application transforms a classical churn model into a **decision intelligence system** that answers a more important question:

> **Is it financially worth acting?**

### Core Capabilities

- ✅ **Churn Prediction** – Precision & Recall optimized models
- ✅ **Adjustable Decision Threshold** – Control prediction sensitivity
- ✅ **Business Integration** – Cost of churn, retention cost, success rate
- ✅ **Action Recommendations** – Personalized retention strategies
- ✅ **ROI Computation** – Financial impact analysis
- ✅ **Portfolio Simulation** – Global strategy optimization
- ✅ **Automatic Threshold Selection** – Optimal strategy discovery

---

## 🧠 Key Features

### 1️⃣ Client-Level Prediction

For a selected client:
- Choose optimization model (Precision / Recall)
- Adjust decision threshold
- Define business assumptions
- **Output:** Churn probability + Recommended actions + Expected financial gain

### 2️⃣ Portfolio-Level ROI Simulation

Analyze strategy impact across entire customer base:
- Compare multiple thresholds
- Compute expected ROI per threshold
- Identify optimal threshold automatically
- Visualize gains through tables and curves
- Identify top at-risk customers

### 3️⃣ Architecture

- **Backend:** FastAPI
- **Database:** PostgreSQL (Neon)
- **Frontend:** Streamlit
- **Orchestration:** Docker Compose
- **ML:** Scikit-learn models (precision & recall tuned)

---

## 📊 Why This Project Is Different

**A model with 90% accuracy can still lose money.**

Traditional ML projects focus on metrics. This system demonstrates how ML must integrate:

1. **Business Constraints** – Real-world cost structures
2. **Financial Modeling** – Expected value calculation
3. **Decision Strategy** – When to act and how

It shifts from _"predicting churn"_ → _"optimizing action strategy"_

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python, FastAPI |
| **Frontend** | Streamlit |
| **ML** | Scikit-learn, Pandas |
| **Database** | PostgreSQL (Neon) / SQLite (dev) |
| **ORM** | SQLAlchemy |
| **Orchestration** | Docker Compose |
| **Deployment** | Hugging Face Spaces |

---

## 📁 Project Structure

```
ProjetChurn/
├── app/                      # FastAPI backend
│   ├── main.py              # API routes
│   ├── schema.py            # Pydantic models
│   ├── db.py                # Database session
│   ├── table_structure.py   # SQLAlchemy models
│   ├── logic.py             # Prediction logic
│   ├── decision_logic.py    # ROI & action logic
│   ├── model/               # Saved ML models
│   └── preprocessing/       # Scaler & encoder
├── ui/                       # Streamlit frontend
│   ├── app.py               # Main page
│   └── pages/               # Feature pages
├── initdb/                   # Database initialization
│   ├── 01create_table.sql   # Schema
│   └── 02fill_table.sql     # Example data
├── test/                     # Pytest tests
│   └── test_api.py          # API tests
├── docker-compose.yml       # Service orchestration
└── readme.md                # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9+ (for local development)

### Quick Start

1. **Clone & Navigate**
   ```bash
   cd ProjetChurn
   ```

2. **Build & Start Services**
   ```bash
   docker compose build --progress=plain
   docker compose up
   ```

3. **Access Applications**
   - **API Docs:** `http://localhost:8000/docs`
   - **Frontend:** `http://localhost:8501`

---

## 🔌 API Endpoints

### Client Management

- `GET /GetClientByIdClient` – Retrieve specific client
- `POST /AddClient` – Create new client
- `DELETE /DeleteClientByIdClient` – Remove client & predictions

### Predictions

- `POST /Decision` – **Main endpoint** – Full decision intelligence
  ```json
  {
    "id_client": 1,
    "option": "precision",
    "threshold": 0.5,
    "churn_cost": 500.0,
    "retention_cost": 50.0,
    "success_rate": 0.3
  }
  ```
- `GET /getPredictionByIdClient` – List client predictions
- `GET /getPredictionByIdPrediction` – Retrieve specific prediction
- `DELETE /deletePredictionByIdPrediction` – Remove prediction

### Analytics

- `GET /GetAllClientByLabel` – Filter clients by churn label

---

## 🧪 Testing

Run pytest suite:

```bash
pytest test/test_api.py -v
```

---

## 📈 Future Improvements

- [ ] Advanced uplift modeling
- [ ] Cost-sensitive learning
- [ ] Automated hyperparameter selection for ROI
- [ ] Multi-segment strategy optimization
- [ ] A/B testing framework integration

---

## 👨‍💻 Author

**Vannel** – AI Engineer specializing in ML & Decision Systems

---

## 📝 License

This project is open-source. Feel free to use and modify.