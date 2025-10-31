import json
import os
import pandas as pd
import joblib
import numpy as np

DATA_PATH = "data/data.csv"
MODEL_PATH = "models/model.pkl"
METRICS_FILE = "metrics.json"
THRESHOLD_ACCURACY = 0.8
EXPECTED_COLUMNS = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']


def test_data_file_exists():
    assert os.path.exists(DATA_PATH), f"{DATA_PATH} missing"


def test_data_columns_and_nulls():
    df = pd.read_csv(DATA_PATH)
    for col in EXPECTED_COLUMNS:
        assert col in df.columns, f"Missing column {col}"
    assert df[EXPECTED_COLUMNS].isnull().sum().sum() == 0, "Dataset contains nulls"


def test_model_file_exists():
    assert os.path.exists(MODEL_PATH), f"{MODEL_PATH} missing"


def test_model_prediction_shape():
    model = joblib.load(MODEL_PATH)
    sample = np.array([[5.1, 3.5, 1.4, 0.2]])
    pred = model.predict(sample)
    assert len(pred) == 1, "Prediction length should be 1"


def test_metrics_file_and_accuracy():
    assert os.path.exists(METRICS_FILE), "metrics.json not found"
    with open(METRICS_FILE, "r") as f:
        metrics = json.load(f)
    acc = metrics.get("accuracy", 0)
    assert acc >= THRESHOLD_ACCURACY, f"Accuracy {acc} below {THRESHOLD_ACCURACY}"