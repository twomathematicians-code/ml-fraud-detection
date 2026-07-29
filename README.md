# 🛡️ ML Fraud Detection System

[![CI/CD](https://github.com/twomathematicians-code/ml-fraud-detection/actions/workflows/ci.yml/badge.svg)](https://github.com/twomathematicians-code/ml-fraud-detection/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://hub.docker.com/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)](https://fastapi.tiangolo.com/)

**Production-grade fraud detection API covering credit card fraud, online payment fraud, and fake news detection — built for real-time scoring in fintech/banking.**

---

## 🎯 Fraud Detection Modules

| Module | Algorithm | Key Features |
|---|---|---|
| **Credit Card Fraud** | XGBoost + SMOTE | Imbalanced learning, real-time scoring, anomaly detection |
| **Online Payment Fraud** | LightGBM + Isolation Forest | Behavioral features, device fingerprinting, velocity checks |
| **Fake News Detection** | DistilBERT + TF-IDF | NLP-based, transformer embeddings, cross-validation |
| **Fake Currency Detection** | ResNet18 Transfer Learning | Image-based, edge deployment ready |

---

## 🏗️ Architecture

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│  FastAPI  │───▶│  Fraud Model  │───▶│PostgreSQL│
│   :8000   │    │  Ensemble     │    │  :5432   │
└──────────┘    └──────────────┘    └──────────┘
      │                                 │
      ▼                                 ▼
┌──────────┐                     ┌──────────┐
│  Redis   │                     │  MLflow  │
│  Cache   │                     │  :5000   │
└──────────┘                     └──────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/twomathematicians-code/ml-fraud-detection.git
cd ml-fraud-detection
docker-compose up --build
```

API available at `http://localhost:8000/docs`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/detect/transaction` | Real-time transaction fraud detection |
| `POST` | `/api/v1/detect/payment` | Online payment fraud check |
| `POST` | `/api/v1/detect/news` | Fake news classification |
| `POST` | `/api/v1/detect/batch` | Batch fraud scoring |
| `GET` | `/api/v1/health` | Health check |

---

## 📊 Performance

| Model | AUC-ROC | Precision | Recall | Latency (ms) |
|---|---|---|---|---|
| Credit Card Fraud (XGBoost) | 0.97 | 0.94 | 0.91 | 12 |
| Payment Fraud (LightGBM) | 0.95 | 0.92 | 0.89 | 8 |
| Fake News (DistilBERT) | 0.96 | 0.93 | 0.94 | 45 |

---

## 👤 Author

**Mahesh Solanki** — [LinkedIn](https://linkedin.com/in/maheshsolanki-16b9a6a5) | [GitHub](https://github.com/twomathematicians-code)
