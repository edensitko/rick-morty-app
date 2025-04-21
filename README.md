# Rick-and-Morty App

This repository contains a complete end-to-end solution for:

1. Extracting data from the Rick and Morty API and saving it to CSV.  
2. Serving the data via a REST API (Flask).  
3. Dockerizing the service.  
4. Deploying on Kubernetes (manifests + Minikube).  
5. Packaging with a Helm chart.  
6. CI/CD with GitHub Actions.

---

## 📂 Directory Structure

```text
rick-morty-app/
├── scripts/                  # Data-extraction script
│   └── fetch_characters.py   # Fetch & filter characters → CSV
├── api-service/              # REST API service
│   ├── app.py                # Flask application
│   ├── requirements.txt      # Python dependencies
│   └── healthcheck.sh        # Healthcheck script (optional)
├── Dockerfile                # Builds the API container
├── yamls/                    # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── helm-chart/               # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
└── .github/workflows/        # CI/CD pipeline
    └── ci-cd.yaml
```

---

## 🛠 Prerequisites

- Docker  
- Minikube  
- Helm  
- Python 3.8+ (for local script & API; can skip if using Docker)  
- `kubectl` CLI

---

## 1. Data Extraction Script

Fetch all **Human**, **Alive** characters whose **origin** is **Earth** and write to `scripts/characters.csv`.

```bash
# (Optional) create & activate virtual environment
cd rick-morty-app
python3 -m venv venv
source venv/bin/activate
pip install requests

# Run the fetch script
cd scripts
env PYTHONPATH="$(pwd)/.." python fetch_characters.py

# Verify
ls -l characters.csv
head -n 5 characters.csv
```

---

## 2. REST API Service

A Flask app exposing `/healthcheck` and `/characters`.

```bash
cd ../api-service
# (In venv)
pip install -r requirements.txt
python app.py              # listens on 0.0.0.0:8080

# In another terminal:
curl http://localhost:8080/healthcheck
curl http://localhost:8080/characters
```

---

## 3. Dockerize the Service

Build & run locally without installing Python on host.

```bash
# From project root:
docker build -t rick-morty-app:dev -f api-service/Dockerfile .

docker run -d --name rm-app -p 8080:80 rick-morty-app:dev
# Test:
curl http://localhost:8080/healthcheck
curl http://localhost:8080/characters

docker stop rm-app && docker rm rm-app
```

---

## 4. Kubernetes Manifests (Minikube)

```bash
minikube start --driver=docker
# Create namespace
kubectl create ns dev --dry-run=client -o yaml | kubectl apply -f -

# Apply manifests
kubectl apply -n dev -f yamls/deployment.yaml
kubectl apply -n dev -f yamls/service.yaml
kubectl apply -n dev -f yamls/ingress.yaml

# Load Docker image into Minikube
minikube image load rick-morty-app:dev

# Expose Ingress via tunnel
sudo minikube tunnel

# Verify & test
kubectl get all -n dev
kubectl get ingress -n dev
curl http://dev.rick-morty.local/healthcheck
curl http://dev.rick-morty.local/characters
```

**Note:** Add entry to `/etc/hosts`:
```bash
echo "$(minikube ip) dev.rick-morty.local" | sudo tee -a /etc/hosts
```

---

## 5. Helm Chart Deployment

```bash
cd helm-chart
helm upgrade --install myapp-dev .   -n dev   --create-namespace   --set image.repository=rick-morty-app   --set image.tag=dev   --set ingress.enabled=true   --set 'ingress.hosts[0].host=dev.rick-morty.local'

# Wait & verify
kubectl rollout status deploy/myapp-dev-rick-morty-app -n dev
kubectl get ingress -n dev
curl http://dev.rick-morty.local/healthcheck
curl http://dev.rick-morty.local/characters
```

---

## 6. CI/CD (GitHub Actions)

See `.github/workflows/ci-cd.yaml` for:
- Bootstrapping KinD cluster  
- Building Docker image  
- Pushing to local registry  
- Deploying with Helm  
- Running smoke tests on endpoints

---

# rick-morty-app
