# Cloud Run API Service
## Cloud Run Local Deployment
### Set GCP Project
```bash
PROJECT_ID=<GCP_PROJECT_ID>
gcloud config set project ${PROJECT_ID}
```

### Build Docker Image via CloudBuild
The CloudBuild job builds the docker image and push it to Google Artifact Registry (GAR) which is run by Cloud Run Service later on.
```bash
SHORT_HASH=$(echo -n "$timestamp" | shasum | cut -c 1-8)
REGION=<REGION>
WORKER_POOL=<WORKER_POOL>
ARTIFACT_REGISTRY_PATH=<ARTIFACT_REGISTRY_PATH>

gcloud builds submit --config=infra/cloudbuild.yaml --region=${REGION} \
--substitutions \_WORKER_POOL=${WORKER_POOL},\
_ARTIFACT_REGISTRY_PATH=${ARTIFACT_REGISTRY_PATH},\
_SHORT_HASH=${SHORT_HASH}
```

### Deploy Cloud Run Service with YAML
Rename `/infra/cloudrun/service-template.yaml` to `service.yaml`.
Replace the variables required for deployments. e.g. PROJECT_ID, LOCATION, etc.
```bash
gcloud run services replace infra/cloudrun/service.yaml
```
