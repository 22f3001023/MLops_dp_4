import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib, json, os

# Paths
data_path = "data/data.csv"
model_dir = "models"
metrics_file = "metrics.json"
os.makedirs(model_dir, exist_ok=True)

print("📥 Loading dataset...")
df = pd.read_csv(data_path)

# Features and target
X = df.drop(columns=["species"])
y = df["species"]

# Split
print("✂️ Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
print("🧠 Training Decision Tree Classifier...")
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Evaluate
print("📊 Evaluating model...")
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

# Save model and metrics
model_path = os.path.join(model_dir, "model.pkl")
joblib.dump(clf, model_path)
with open(metrics_file, "w") as f:
    json.dump({"accuracy": acc, "report": report}, f, indent=4)

print(f"✅ Model saved at: {model_path}")
print(f"✅ Accuracy: {acc:.4f}")
