import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import os

def save_metrics(metrics, metrics_path):
    """
    Saves metrics to a JSON file.
    """
    # Ensure the directory for metrics exists
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

def training(data, model_path):
    """
    Trains the model and saves it.
    """
    # Split features and target
    X = data.drop(columns=["species"])
    y = data["species"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y
