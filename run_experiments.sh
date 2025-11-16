#!/bin/bash
# This script stops if any command fails
set -e

# --- 1. CREATE DATA ---
echo "--- Step 1: Creating datasets ---"
python create_poisoned_data.py

# --- 2. TRACK DATA WITH DVC ---
echo "--- Step 2: Tracking data with DVC ---"
dvc add data/iris_original.csv
dvc add data/iris_poisoned_5.csv
dvc add data/iris_poisoned_10.csv
dvc add data/iris_poisoned_50.csv

# --- 3. RUN EXPERIMENTS & TRACK MODELS ---
echo "--- Step 3: Running MLFlow experiments ---"
EXP_NAME="Week 8 Poisoning"

# Run 1: 0% Poison (Original)
echo "Running 0% poison experiment..."
# The python script will print the model path, and we capture it
model_0_path=$(python train.py data/iris_original.csv "$EXP_NAME" "poison_0_percent")
dvc add $model_0_path

# Run 2: 5% Poison
echo "Running 5% poison experiment..."
model_5_path=$(python train.py data/iris_poisoned_5.csv "$EXP_NAME" "poison_5_percent")
dvc add $model_5_path

# Run 3: 10% Poison
echo "Running 10% poison experiment..."
model_10_path=$(python train.py data/iris_poisoned_10.csv "$EXP_NAME" "poison_10_percent")
dvc add $model_10_path

# Run 4: 50% Poison
echo "Running 50% poison experiment..."
model_50_path=$(python train.py data/iris_poisoned_50.csv "$EXP_NAME" "poison_50_percent")
dvc add $model_50_path


# --- 4. COMMIT AND PUSH ---
echo "--- Step 4: Committing to Git and pushing DVC data ---"
# Add all the new .dvc files and code to git
git add .

# Check if there's anything to commit
if git diff-index --quiet HEAD --; then
    echo "No changes to commit. Exiting."
else
    git commit -m "Run Week 8 poisoning experiments"
    echo "Committed experiment files to Git."
fi

# Push data to DVC remote (GCS)
dvc push

echo "--- All Done! ---"
echo "Run 'mlflow ui' in your terminal to see the results."
