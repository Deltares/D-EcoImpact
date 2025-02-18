#!/bin/bash
export IMAGE_ID="decoimpact"
export VERSION="latest"
export ARTIFACT_REGISTRY_URL="ghcr.io/deltares"
export TAG="${ARTIFACT_REGISTRY_URL}/${IMAGE_ID}:${VERSION}"
docker build . --file Dockerfile --tag "${TAG}"
## Pushes image to Artifact Registry
docker push "${TAG}"
