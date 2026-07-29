#!/usr/bin/env python3
"""Fraud detection training pipeline — XGBoost + Isolation Forest ensemble."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml, logging
from src.models.train import FraudModelTrainer

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger("fraud-pipeline")

    with open("configs/model_config.yaml") as f:
        cfg = yaml.safe_load(f)

    logger.info("Initializing FraudModelTrainer...")
    trainer = FraudModelTrainer(
        contamination=cfg["detection"]["anomaly_contamination"],
        random_state=42,
    )

    # Simulated training data — replace with real dataset
    import numpy as np
    np.random.seed(42)
    n_samples = 10000
    transactions = [
        {"amount": np.random.exponential(200), "merchant_category": "retail",
         "device_fingerprint": "dev_" + str(i), "hour_of_day": i % 24,
         "day_of_week": i % 7, "tx_velocity_1h": np.random.poisson(2),
         "tx_velocity_24h": np.random.poisson(8), "customer_avg_amount": 150,
         "distinct_merchants_24h": np.random.randint(1, 15),
         "amount_deviation_from_mean": np.random.normal(0, 500)}
        for i in range(n_samples)
    ]
    labels = [1 if np.random.random() < 0.01 else 0 for _ in range(n_samples)]

    logger.info("Training ensemble model on %d transactions...", n_samples)
    metrics = trainer.fit(transactions, labels)
    logger.info("Training complete. CV AUC-PR: %.4f (±%.4f)", metrics["cv_aucpr_mean"], metrics["cv_aucpr_std"])

    # Score sample
    sample = transactions[:5]
    preds = trainer.predict(sample)
    for i, p in enumerate(preds):
        logger.info("Sample %d → fraud_prob=%.4f, risk=%s", i, p["fraud_probability"], p["risk_level"])

if __name__ == "__main__":
    main()
