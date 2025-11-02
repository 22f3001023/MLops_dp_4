MLOps CI/CD Pipeline for Iris Classifier
This repository demonstrates a complete, end-to-end MLOps workflow for training, testing, and deploying a machine learning model. The project uses an Iris classifier (Decision Tree) and implements a full CI/CD pipeline using GitHub Actions to deploy the model as an API on Google Kubernetes Engine (GKE).
This project fulfills the requirements for an MLOps assignment, showing the integration of:
Continuous Integration (CI): Automated training and testing.
Continuous Deployment (CD): Automated containerization, registry push, and deployment to Kubernetes.
Pipeline Status
Pipeline Architecture
The workflow is broken into two main pipelines, both triggered on a push to the main branch.
1. Continuous Integration (CI) - ci.yml
This pipeline is responsible for ensuring the code, model, and data are valid.
Checkout Code: Clones the repository.
Setup Python & Install Dependencies: Prepares the environment from requirements.txt.
Run Training: Executes src/main.py to train the model and generate models/model.pkl and metrics.json.
Run Tests: Runs pytest to validate:
The data file exists.
The data has the correct columns.
The trained model.pkl file was created.
The metrics.json file was created and accuracy is acceptable.
2. Continuous Deployment (CD) - cd.yml
This pipeline is responsible for building and deploying the model as a production-ready API. It consists of two jobs:
Job 1: build-and-push
Checkout Code: Clones the repository.
Authenticate to GCP: Logs into Google Cloud using a Service Account Key.
Configure Docker: Sets up authentication for Google Artifact Registry (GAR).
Build & Tag Image: Builds a Docker image from the Dockerfile (which contains the Flask API in src/app.py) and tags it with the unique commit SHA.
Push to GAR: Pushes the container image to the Google Artifact Registry.
Job 2: deploy-to-gke (Depends on the build-and-push job)
Checkout Code: Clones the repository.
Authenticate to GCP: Logs into Google Cloud.
Get GKE Credentials: Connects kubectl to the target GKE cluster (autopilot-cluster-1).
Replace Image Placeholder: Uses a GitHub Action (cschleiden/replace-tokens) to dynamically find the __IMAGE_URL__ placeholder in .k8s/deployment.yml and replace it with the actual image path from the previous job.
Deploy to GKE: Runs kubectl apply -f .k8s/deployment.yml to deploy the new version of the application to Kubernetes. The Kubernetes Service of type: LoadBalancer then exposes it to the internet.
Technologies Used
ML/Data: Python, Pandas, Scikit-learn
CI/CD: GitHub Actions
API: Flask
Testing: Pytest
Containerization: Docker
Cloud & Orchestration: Google Cloud Platform (GCP)
Google Kubernetes Engine (GKE): For running the application at scale.
Google Artifact Registry (GAR): For storing Docker container images.
Repository Structure
.
├── .github/workflows/
│   ├── ci.yml           # CI: Runs training and tests
│   └── cd.yml           # CD: Builds, pushes, and deploys to GKE
├── .k8s/
│   └── deployment.yml   # Kubernetes manifests (Deployment & Service)
├── data/
│   └── data.csv         # The Iris dataset
├── models/
│   └── .gitignore       # Trained models are git-ignored
├── src/
│   ├── app.py           # Flask API server
│   ├── main.py          # Main script to run training
│   └── training/
│       └── train.py     # Core training and evaluation logic
├── tests/
│   └── test_validation... # Pytest script for CI
├── Dockerfile           # Recipe to build the Flask API container
├── metrics.json         # (Git-ignored) Model metrics
└── requirements.txt     # Python dependencies


