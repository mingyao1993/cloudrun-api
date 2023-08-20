# Cloud Run API Service

Welcome to this repository that offers a demonstration to test, build
, and local deployment of a basic Cloud Run API service to Google Cloud Platform environment.

The main features of this repository include:

- Local CLI deployment of a single service housing two distinct API endpoints via GCP CloudBuild.
- The first endpoint functions as a fundamental health check.
- The second endpoint facilitates an asynchronous, fund transfer transaction process. 
This process seamlessly integrates the PubSub messaging service and the Datastore NoSQL document database for efficient communication and data storage.

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
