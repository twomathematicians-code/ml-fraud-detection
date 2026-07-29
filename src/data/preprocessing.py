"""Fraud data preprocessing — imbalance handling & velocity features."""
import numpy as np; import pandas as pd
from sklearn.preprocessing import RobustScaler, LabelEncoder
from imblearn.over_sampling import SMOTE

class FraudDataPreprocessor:
    def __init__(self): self.scaler = RobustScaler(); self.encoders = {}
    def fit_transform(self, df: pd.DataFrame, target_col: str = "is_fraud"):
        df = df.copy()
        for col in df.select_dtypes(include=["object","category"]).columns:
            if col != target_col: self.encoders[col] = LabelEncoder(); df[col] = self.encoders[col].fit_transform(df[col].astype(str))
        X = df.drop(columns=[target_col]) if target_col in df.columns else df
        y = df[target_col] if target_col in df.columns else None
        Xs = pd.DataFrame(self.scaler.fit_transform(X), columns=X.columns)
        if y is not None and y.mean() < 0.05:
            sm = SMOTE(sampling_strategy=0.1, random_state=42, k_neighbors=5)
            Xr, yr = sm.fit_resample(Xs, y); return Xr, yr
        return Xs, y
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col, le in self.encoders.items():
            if col in df.columns: df[col] = le.transform(df[col].astype(str))
        return pd.DataFrame(self.scaler.transform(df), columns=df.columns)
