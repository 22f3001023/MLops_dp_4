import pandas as pd
import joblib
import sys
import os
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

def train_model(data_path, experiment_name, run_name):
    """Trains a model and logs metrics and artifacts to MLFlow."""
    
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(run_name=run_name):
        # 1. Load Data
        df = pd.read_csv(data_path)
        X = df.drop('target', axis=1)
        y = df['target']
        
        # 2. Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # 3. Log Parameters
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", 100)

        # 4. Train Model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # 5. Evaluate Model
        preds = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, average='weighted')
        recall = recall_score(y_test, preds, average='weighted')
        
        # 6. Log Metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        
        # --- THIS IS THE FIX ---
        # Print status messages to stderr so the shell script doesn't capture them
        print(f"Run: {run_name} | Accuracy: {accuracy:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f}", file=sys.stderr)

        # 7. Log Model Artifact
        mlflow.sklearn.log_model(model, "model")
        
        # 8. Save model with joblib
        os.makedirs('models', exist_ok=True)
        model_filename = f"models/model_{run_name}.joblib"
        joblib.dump(model, model_filename)
        
        mlflow.log_artifact(model_filename)
        
        # Return the path for the main block to print
        return model_filename

if __name__ == "__main__":
    if len(sys.argv) != 4:
        # Print usage errors to stderr
        print("Usage: python train.py <data_path> <experiment_name> <run_name>", file=sys.stderr)
        sys.exit(1)
        
    data_path = sys.argv[1]
    experiment_name = sys.argv[2]
    run_name = sys.argv[3]
    
    # Run the function
    model_filename = train_model(data_path, experiment_name, run_name)
    
    # --- THIS IS THE FIX ---
    # Print *only* the filename to stdout so the shell script can capture it
    print(model_filename)
