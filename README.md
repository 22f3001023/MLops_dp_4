

# MLOps Week 8 Assignment: Data Poisoning & Experiment Tracking

This project demonstrates a pipeline for a data poisoning experiment on the IRIS dataset. It uses DVC to version data and models, and MLFlow to log and compare the validation outcomes of models trained on data with varying levels of corruption.

## 🎯 Assignment Objective

> Integrate data poisoning for IRIS using randomly generated numbers at various levels(5%, 10%, 50%) and explain the validation outcomes when trained on such data using MLFlow. Give your thoughts on how to mitigate such a poisoning attacks and how data quantity requirements evolve when data quality is affected. [cite: 181]

-----

## 🛠️ Tech Stack

  * **Data Versioning:** DVC (Data Version Control) [cite: 186, 187]
  * **Experiment Tracking:** MLFlow [cite: 181]
  * **Cloud Storage:** Google Cloud Storage (GCS) (as DVC remote) [cite: 187]
  * **Training:** Python, Pandas, Scikit-learn
  * **Automation:** Bash (`run_experiments.sh`)

-----

## 📂 Project Pipeline

The experiment is orchestrated by a single script, `run_experiments.sh`, which performs the following steps:

1.  **`create_poisoned_data.py`:** Loads the original IRIS dataset, injects label noise at 5%, 10%, and 50% levels, and saves four distinct CSV files (`iris_original.csv`, `iris_poisoned_5.csv`, etc.).
2.  **`dvc add`:** The script versions all four new datasets using DVC.
3.  **`train.py`:** This MLFlow-integrated script is called four times. It trains a RandomForestClassifier on each dataset, logging all parameters (like `data_path`) and metrics (accuracy, precision, recall) to MLFlow.
4.  **`dvc add`:** After each model is trained, it is versioned by DVC.
5.  **`git commit`:** The script commits all new `.dvc` files to Git.
6.  **`dvc push`:** All DVC-tracked data and models are pushed to the Google Cloud Storage remote.

-----

## 🚀 How to Run the Experiment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/22f3001023/MLops_dp_4.git
    cd MLops_dp_4
    ```
2.  **Set up the environment:**
    ```bash
    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    ```
3.  **Authenticate with GCS:** (Required for DVC to push/pull)
    ```bash
    gcloud auth application-default login
    ```
4.  **Run the full experiment:**
    ```bash
    # Make the script executable
    chmod +x run_experiments.sh

    # Run the pipeline
    ./run_experiments.sh
    ```
5.  **View the results in MLFlow:**
      * **If running on a remote VM:** You must first create an SSH tunnel from your local machine.
        ```bash
        # On your LOCAL machine (e.g., PowerShell/Terminal)
        gcloud compute ssh YOUR_INSTANCE_NAME --zone=YOUR_ZONE -- -L 8080:localhost:5000
        ```
      * **In your instance terminal:** Run the MLFlow UI.
        ```bash
        # In your INSTANCE terminal
        mlflow ui
        ```
      * Open **`http://localhost:8080`** in your **local** web browser to see the dashboard.

-----

## 📊 Results & Validation Outcomes

The experiment was tracked using MLFlow. By comparing the four runs, we can clearly see the direct impact of data poisoning on model performance.

| Run Name | Data Source | Accuracy | Precision | Recall |
| :--- | :--- | :--- | :--- | :--- |
| `poison_0_percent` | `iris_original.csv` | **1.0** | 1.0 | 1.0 |
| `poison_5_percent` | `iris_poisoned_5.csv` | **0.933** | 0.935 | 0.933 |
| `poison_10_percent`| `iris_poisoned_10.csv` | **0.800** | 0.803 | 0.800 |
| `poison_50_percent`| `iris_poisoned_50.csv` | **0.444** | 0.461 | 0.444 |

### Explanation:

As shown in the MLFlow results, the model's accuracy degrades significantly as the percentage of poisoned data (corrupted labels) increases.

  * **Baseline:** The model on clean data achieves 100% accuracy.
  * **5% Poisoning:** A small 5% corruption drops the accuracy by \~7%.
  * **10% Poisoning:** The accuracy falls to 80% as the model starts learning incorrect patterns.
  * **50% Poisoning:** The data is so corrupt that the model is completely confused, and its accuracy plummets to 44.4%, which is worse than random guessing for a 3-class problem.

-----

## 💡 Mitigation & Key Takeaways

### How to Mitigate Poisoning Attacks

1.  **Data Validation Pipelines:** The best defense is to catch bad data *before* training. We can add automated steps to our CI pipeline (like GitHub Actions [cite: 189]) to validate incoming data. These checks can look for sudden shifts in label distribution or other statistical anomalies.
2.  **Outlier Detection:** Run anomaly detection algorithms on the training data to find and flag samples that are statistically different from the rest. These are often the poisoned samples.
3.  **Data Versioning (DVC):** As demonstrated in this project, DVC itself is a mitigation tool[cite: 186]. By versioning our data, if we observe a sudden model performance drop, we can instantly roll back (`dvc checkout`) to a previous "known-good" version of the data and investigate what changed[cite: 188].

### Data Quality vs. Quantity

This experiment proves that **data quality is far more important than data quantity.**

A model trained on just 150 high-quality rows performed perfectly (100% accuracy). However, introducing just 15 bad data points (10%) crippled the model. Having 10,000 rows of low-quality, poisoned data would be significantly worse than 1,000 rows of clean, verified data.
