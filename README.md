
# API Buffering System
[![Lint and test](https://github.com/Yikuan-Tu/api-buffering-system/actions/workflows/ci.yml/badge.svg)](https://github.com/Yikuan-Tu/api-buffering-system/actions/workflows/ci.yml)

A FastAPI-based service that buffers person records in memory and flushes them to SQLite when reaching a configurable buffer size (defaults to 100).

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
  - [Method 1: Local Development](#method-1-local-development)
  - [Method 2: Dockerized Deployment](#method-2-dockerized-deployment)
  - [Method 3: Kubernetes Deployment](#method-3-kubernetes-deployment)
- [Testing](#testing)
- [CI/CD Workflow](#cicd-workflow)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Cleanup](#cleanup)

## Features
- REST API with `/submit` endpoint
- In-memory buffering with automatic flush to SQLite
- Configurable buffer size
- Docker and Kubernetes support
- Comprehensive test suite

## Prerequisites
- [Python](https://www.python.org/downloads/) 3.11+
- [Docker Desktop](https://docs.docker.com/desktop/) (for containerized deployment)
- [Docker Compose](https://docs.docker.com/compose/install/) (for containerized deployment using `docker-compose` only)
- [kubectl](https://pwittrock.github.io/docs/tasks/tools/install-kubectl/) and [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for Kubernetes deployment)

## Setup
```bash
git clone https://github.com/Yikuan-Tu/api-buffering-system.git
cd api-buffering-system

# Create the .env file with the required environment variables
echo "DB_PATH=./data/database.db
BUFFER_SIZE=100
LOG_LEVEL=INFO" > .env

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt
```

## Running the Application

### Method 1: Local Development
```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Access API at http://localhost:8000

# In another terminal, run test suite
pytest tests/ -v

# Run the load test script
python tests/test_submit.py
```

### Method 2: Dockerized Deployment

#### Using Docker Compose:
```bash
# Build and start api server
docker-compose up api

# Access API at http://localhost:8000

## In another terminal
# Run test suite in container
docker-compose run tests

# Run the load test script against container
python tests/test_submit.py
```

#### Using Plain Docker:
```bash
# Build the image
docker build -t api-buffering-system --target production .

# Run the container
docker run -p 8000:8000 api-buffering-system

# Access API at http://localhost:8000

# In another terminal, run the load test script against container
python tests/test_submit.py
```

### Method 3: Kubernetes Deployment
```bash
# Start Minikube
minikube start --profile=dev-cluster

# Build image in Minikube's Docker context
eval $(minikube docker-env)
docker build -t api-buffering-system:latest --target production .

# Deploy to Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/

# Access the service
kubectl port-forward svc/api-buffering-system 8000:8000 -n api-buffering-system

# Run load test script against cluster
python tests/test_submit.py
```

## Testing

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Load Testing
```bash
python tests/test_submit.py
```

## CI/CD Workflow
The GitHub Actions workflow (`/.github/workflows/ci.yml`) performs:
1. Code checkout
2. Python 3.11 setup
3. Linting checks (Black and Ruff)
4. Automated Unit and integration tests

## API Endpoints
- `GET /`: Welcome message
- `GET /health/`: Health check
- `GET /docs/`:  Swagger page for API reference
- `GET /count/`: Current record count in database
- `POST /submit/`: Submit person records (JSON array)

Example request:
```bash
curl -X POST http://localhost:8000/submit/ \
  -H "Content-Type: application/json" \
  -d '[{"first_name":"John","last_name":"Doe"}]'
```

## Configuration
Environment variables:
- `DB_PATH`: Database file path (default: `/data/database.db`)
- `BUFFER_SIZE`: Records before flush (default: `100`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Cleanup

### Docker
```bash
docker-compose down -v
```

### Kubernetes
```bash
kubectl delete -f k8s/
minikube stop --profile=dev-cluster
minikube delete --profile=dev-cluster
```
