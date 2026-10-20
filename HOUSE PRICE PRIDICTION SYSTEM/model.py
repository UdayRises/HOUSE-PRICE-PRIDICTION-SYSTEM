"""
Trains a house price prediction model and saves it (with its preprocessing
pipeline) to model/house_price_model.pkl for the Flask app to load.
"""
import json
import os
import time

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# 1. Use dynamic paths relative to the script location (matching app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "housing.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "house_price_model.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

NUMERIC_FEATURES = [
    "GrLivArea", "LotArea", "TotalBsmtSF", "OverallQual", "OverallCond",
    "YearBuilt", "BedroomAbvGr", "FullBath", "HalfBath", "GarageCars",
    "Fireplaces",
]
CATEGORICAL_FEATURES = ["Neighborhood", "HouseStyle", "CentralAir"]
TARGET = "SalePrice"


def train_and_save_model(data_path=DATA_PATH, model_path=MODEL_PATH, metrics_path=METRICS_PATH):
    """Trains the house price prediction pipeline and saves the model artifact and metrics."""
    # Ensure data directory and file exist
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Auto-generating training data...")
        from data import generate_and_save
        generate_and_save(data_path)

    df = pd.read_csv(data_path)
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(transformers=[
        ("num", "passthrough", NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    t0 = time.time()
    pipeline.fit(X_train, y_train)
    train_time = time.time() - t0

    preds = pipeline.predict(X_test)
    rmse = root_mean_squared_error(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = {
        "rmse": round(float(rmse), 2),
        "mae": round(float(mae), 2),
        "r2": round(float(r2), 4),
        "train_time_sec": round(train_time, 2),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }

    model_dir = os.path.dirname(os.path.abspath(model_path))
    os.makedirs(model_dir, exist_ok=True)

    bundle = {
        "pipeline": pipeline,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "neighborhoods": sorted(df["Neighborhood"].unique().tolist()),
        "house_styles": sorted(df["HouseStyle"].unique().tolist()),
    }

    joblib.dump(bundle, model_path)

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return bundle, metrics


def main():
    bundle, metrics = train_and_save_model()
    print("Training complete.")
    print(json.dumps(metrics, indent=2))
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()