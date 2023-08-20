# Cloud Run API Service

## Prerequisite
- Python
- Docker
- GCP (deployment)

## Local Testing with Docker

Run docker-compose command to build and spin up main app, pubsub emulator and datastore emulator containers.
```bash
docker-compose -f docker-compose.yml up -d
```

Run unit test on the docker container
```bash
docker exec mloh-sandbox /bin/sh -c "poetry run pytest /home/appuser/tests/unit_tests/ -disable-warnings -vv -s
```

integration test on the docker container
```bash
docker exec mloh-sandbox /bin/sh -c "poetry run pytest /home/appuser/tests/unit_tests/ -disable-warnings -vv -s
```

## Cloud Run Local Deployment

### Set GCP Project

```bash
PROJECT_ID=<GCP_PROJECT_ID>
gcloud config set project ${PROJECT_ID}
```

### Build Docker Image via CloudBuild

The CloudBuild job tests and builds the docker image and push it to Google Artifact Registry (GAR) which is run by Cloud Run
Service later on.

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
