import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import os 

def training(data, model_path):
    X = data.drop(columns=["species"])
    y = data["species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # ------------------
    # ⬇️ 2. THIS IS THE FIX ⬇️
    # ------------------
    # Create the 'models/' directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the model
    joblib.dump(clf, model_path)
    return acc, report
