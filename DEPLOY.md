# Deployment Guide

This document provides instructions for deploying the Flask CRUD application to various environments.

## Prerequisites

- Docker
- Kubernetes cluster (1.20+)
- kubectl configured
- GitHub Actions enabled (for CI/CD)

## Local Development

### Using Docker Compose

```bash
docker-compose up -d
```

Visit `http://localhost:5000`

### Using Python (Development)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Docker Build

### Build locally

```bash
docker build -t flask-crud-app:latest .
docker run -p 5000:5000 flask-crud-app:latest
```

### Push to registry

```bash
docker tag flask-crud-app:latest ghcr.io/your-username/flask-app:latest
docker push ghcr.io/your-username/flask-app:latest
```

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 2. Deploy with Kustomize

```bash
kubectl apply -k k8s/
```

### 3. Deploy with Individual Manifests

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

### 4. Verify Deployment

```bash
kubectl get pods -n flask-apps
kubectl get svc -n flask-apps
kubectl describe deployment flask-flask-crud-app -n flask-apps
```

### 5. Monitor Pod Status

```bash
kubectl logs -n flask-apps -l app=flask-crud-app -f
```

## GitHub Actions CI/CD

The workflow automatically:
1. Runs on push/PR to main and develop branches
2. Tests the application
3. Builds Docker image
4. Pushes to GitHub Container Registry
5. Deploys to Kubernetes (on main branch push)

### Setup

1. Configure git secrets for your registry
2. Update image registry in workflow files
3. Set up kubeconfig for deployment

### Trigger Workflow

```bash
git push origin main
```

## Accessing the Application

### Local
- http://localhost:5000

### Kubernetes (Port Forward)
```bash
kubectl port-forward -n flask-apps svc/flask-crud-app 5000:80
```
Then visit http://localhost:5000

### Via Ingress
- https://flask-app.example.com (update domain in ingress.yaml)

## Database Persistence

Currently uses SQLite. For production, consider:

1. **PostgreSQL** (recommended)
   - Create a separate PostgreSQL deployment
   - Update DATABASE_URL in configmap
   - Add init job for migrations

2. **Persistent Volume**
   - Mount PV for SQLite database

## Scaling

The deployment includes HPA (Horizontal Pod Autoscaler):
- Min replicas: 2
- Max replicas: 10
- Scales on CPU (70%) and Memory (80%) utilization

Check HPA status:
```bash
kubectl get hpa -n flask-apps
kubectl describe hpa flask-flask-crud-app -n flask-apps
```

## Troubleshooting

### Check pod logs
```bash
kubectl logs -n flask-apps <pod-name>
```

### Describe pod for events
```bash
kubectl describe pod -n flask-apps <pod-name>
```

### Check deployment status
```bash
kubectl rollout status deployment/flask-flask-crud-app -n flask-apps
```

### Rollback deployment
```bash
kubectl rollout undo deployment/flask-flask-crud-app -n flask-apps
```

## Security Notes

- Non-root user (UID: 1000) used in container
- Resource limits enforced
- Liveness and readiness probes configured
- Pod disruption budget recommended for production

## Next Steps

1. Update image registry references
2. Configure domain in ingress.yaml
3. Set up cert-manager for TLS
4. Add database backup strategy
5. Configure monitoring (Prometheus/Grafana)
6. Add logging aggregation (ELK/Loki)
