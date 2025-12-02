# Kubernetes Configurations for BAP BE Bot

This directory contains Kubernetes configurations for deploying the Discord and Telegram bots using Kustomize.

## Directory Structure

```
k8s/
├── base/                  # Base configurations
│   ├── kustomization.yaml # With namespace: bap-be-bot
│   ├── secret.yaml        # Parameterized secret template
│   └── deployment.yaml    # Combined Discord and Telegram deployments
└── overlays/              # Environment-specific overlays
    ├── dev/               # Development environment
    │   ├── kustomization.yaml # With namespace: bap-be-bot-dev
    │   └── .env.example
    └── prod/              # Production environment
        ├── kustomization.yaml # With namespace: bap-be-bot-prod
        └── .env.example
```

## Usage

### Prerequisites

- Kubernetes cluster
- kubectl installed
- kustomize installed (or use kubectl built-in kustomize)

### Deployment Steps

1. Navigate to the environment directory you want to deploy (e.g., `k8s/overlays/dev/`)
2. Create a `.env` file with your environment variables:
   ```
   cp .env.example .env
   ```
3. Edit the `.env` file and fill in your API keys and tokens
4. Deploy using kustomize:
   ```
   kubectl apply -k .
   ```
   Or with kubectl's built-in kustomize:
   ```
   kubectl kustomize . | kubectl apply -f -
   ```

### Secret Management

Secrets are managed using Kustomize's `secretGenerator` feature. The environment variables are loaded from the `.env` file in each overlay directory.

### Namespace Management

Each environment uses a dedicated namespace:
- Base: `bap-be-bot`
- Dev: `bap-be-bot-dev`
- Prod: `bap-be-bot-prod`

### Adding New Environments

To add a new environment (e.g., staging):

1. Create a new directory under `overlays/` (e.g., `k8s/overlays/staging/`)
2. Copy the kustomization.yaml and .env.example files from an existing environment
3. Update the namespace in kustomization.yaml (e.g., `namespace: bap-be-bot-staging`)
4. Create a `.env` file with the appropriate environment variables

## Resource Requirements

- Discord Bot:
  - Requests: 100m CPU, 256Mi memory
  - Limits: 500m CPU, 512Mi memory

- Telegram Bot:
  - Requests: 100m CPU, 256Mi memory
  - Limits: 500m CPU, 512Mi memory

## CI/CD Integration

A GitHub Actions workflow is provided in `.github/workflows/deploy.yaml` that:
1. Builds and pushes the Docker image with a unique SHA tag
2. Updates the Kustomize configurations with the new image
3. Deploys to all environments (dev and prod)
4. Injects secrets from GitHub Secrets as environment variables
