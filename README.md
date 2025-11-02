Here’s a cleaned-up and professional version formatted as a full `README.md` file for your Iris Classifier MLOps project.

***

# Iris Classifier MLOps CI/CD Pipeline

This repository demonstrates a complete, end-to-end **MLOps workflow** for training, testing, and deploying a machine learning model using a Decision Tree classifier on the Iris dataset. It implements fully automated **Continuous Integration (CI)** and **Continuous Deployment (CD)** pipelines using **GitHub Actions**, deploying the final model as an API to **Google Kubernetes Engine (GKE)**.

***

## Pipeline Overview

This project fulfills the core requirements of an MLOps system by integrating:

- **Continuous Integration (CI):** Automated training, testing, and validation.
- **Continuous Deployment (CD):** Automated containerization, image push, and Kubernetes deployment.

Two main workflows are triggered automatically on each push to the `main` branch.

***

## 1. Continuous Integration (CI) – `.github/workflows/ci.yml`

The CI pipeline ensures that the model, data, and codebase are valid before deployment.

### Steps

- **Checkout Code:** Clones the repository.
- **Setup Environment:** Installs Python and dependencies from `requirements.txt`.
- **Run Training:** Executes `src/main.py` to train the model and save:
  - `models/model.pkl` – serialized Decision Tree model.
  - `metrics.json` – model performance metrics.
- **Run Tests (Pytest):** Validates:
  - Presence and correctness of the data file.
  - Correct column structure in `data.csv`.
  - Existence of the trained `model.pkl` file.
  - Creation and accuracy threshold in `metrics.json`.

***

## 2. Continuous Deployment (CD) – `.github/workflows/cd.yml`

The CD pipeline builds a container image for the trained model, pushes it to **Google Artifact Registry (GAR)**, and deploys it to **GKE**.

### Job 1: `build-and-push`

- **Checkout Code**  
  Clones the repository.

- **Authenticate to GCP**  
  Uses a Google Cloud Service Account Key for authentication.

- **Configure Docker for GAR**  
  Enables Docker to push images securely.

- **Build & Tag Docker Image**  
  Builds a container image from the `Dockerfile`, tagging it with the commit SHA.

- **Push to Artifact Registry**  
  Pushes the image to Google Artifact Registry.

### Job 2: `deploy-to-gke` (depends on `build-and-push`)

- **Checkout Code**  
  Clones the repository again for deployment.

- **Authenticate to GCP**  
  Re-authenticates the workflow with the service account.

- **Get GKE Credentials**  
  Configures `kubectl` to connect to the GKE cluster (`autopilot-cluster-1`).

- **Replace Image Placeholder**  
  Dynamically replaces the `__IMAGE_URL__` placeholder in `.k8s/deployment.yml` with the new image path using the GitHub Action `cschleiden/replace-tokens`.

- **Deploy to GKE**  
  Executes `kubectl apply -f .k8s/deployment.yml` to deploy the updated image.  
  The Kubernetes **Service (LoadBalancer)** exposes the Flask API to external users.

***

## Technologies Used

| Domain | Technologies |
|---------|---------------|
| **ML / Data** | Python, Pandas, Scikit-learn |
| **API** | Flask |
| **Testing** | Pytest |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker |
| **Cloud Platform** | Google Cloud Platform (GCP) |
| **Orchestration** | Google Kubernetes Engine (GKE) |
| **Registry** | Google Artifact Registry (GAR) |

***

## Repository Structure

```
.
├── .github/workflows/
│   ├── ci.yml              # CI: Training and testing workflow
│   └── cd.yml              # CD: Build, push, and deploy workflow
├── .k8s/
│   └── deployment.yml      # Kubernetes Deployment and Service definitions
├── data/
│   └── data.csv            # Iris dataset
├── models/
│   └── .gitignore          # Excludes trained models from version control
├── src/
│   ├── app.py              # Flask API server
│   ├── main.py             # Entry point for model training
│   └── training/
│       └── train.py        # Core training and evaluation logic
├── tests/
│   └── test_validation.py  # Pytest scripts for validation
├── Dockerfile              # API container build configuration
├── metrics.json            # Model evaluation metrics (ignored in git)
└── requirements.txt        # Python dependencies
```

***

## Deployment Architecture

1. **Developer pushes code → GitHub Action triggers.**  
2. **CI pipeline** runs tests, training, and validation.  
3. Upon success, **CD pipeline** builds and pushes the image to GAR.  
4. The image is deployed to **GKE** and exposed as a LoadBalancer service.  
5. The API becomes accessible via an external IP endpoint.

***

## Outputs

- Trained model: `models/model.pkl`
- Model metrics: `metrics.json`
- Live API endpoint via GKE LoadBalancer

***

Would you like a short “Quick Start” section added to guide users through setting up GCP authentication and running the pipeline locally?
