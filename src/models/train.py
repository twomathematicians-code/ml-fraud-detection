"""Fraud Detection — XGBoost + Isolation Forest ensemble."""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import StratifiedKFold, cross_val_score
from xgboost import XGBClassifier

class FraudModelTrainer:
    def __init__(self, contamination=0.01, random_state=42):
        self.anomaly = IsolationForest(contamination=contamination, random_state=random_state, n_jobs=-1)
        self.clf = XGBClassifier(scale_pos_weight=99, max_depth=6, learning_rate=0.05, n_estimators=200,
            subsample=0.8, colsample_bytree=0.8, random_state=random_state, eval_metric="aucpr")

    def extract_features(self, txs):
        feats = []
        for tx in txs:
            feats.append([np.log(float(tx.get("amount",1))+1), hash(str(tx.get("merchant_category","")))%1000/1000,
                len(str(tx.get("device_fingerprint","")))/64, float(tx.get("hour_of_day",12))/24,
                float(tx.get("day_of_week",3))/7, float(tx.get("tx_velocity_1h",0))/50])
        return np.array(feats)

    def fit(self, txs, labels):
        X = self.extract_features(txs); y = np.array(labels)
        self.anomaly.fit(X); self.clf.fit(X, y)
        scores = cross_val_score(self.clf, X, y, cv=StratifiedKFold(5), scoring="average_precision")
        return {"cv_aucpr_mean": float(scores.mean()), "cv_aucpr_std": float(scores.std())}

    def predict(self, txs):
        X = self.extract_features(txs); anom = -self.anomaly.score_samples(X); probs = self.clf.predict_proba(X)[:,1]
        return [{"fraud_probability": float(probs[i]), "anomaly_score": float(anom[i]),
            "risk_level": "critical" if probs[i]>0.8 else "high" if probs[i]>0.5 else "low"} for i in range(len(txs))]
