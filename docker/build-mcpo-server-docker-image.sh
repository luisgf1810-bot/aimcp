#!/bin/bash
set -eo pipefail

Dockerfile_PATH="./Dockerfile.MCPO-Proxy"
IMAGE_NAME="mcpo-proxy"

echo "=== Building Docker image Name: ${IMAGE_NAME} ==="

VERSION="1.0"
TAGs="latest"

# Build once with version tag
docker build -t ${IMAGE_NAME}:${VERSION} -f ${Dockerfile_PATH} .

# Tag as latest
for TAG in ${TAGs}
do
    docker tag ${IMAGE_NAME}:${VERSION} ${IMAGE_NAME}:${TAG}
done

