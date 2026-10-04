#!/bin/bash
set -e

# Configuration (Change 'your-dockerhub-username' to your actual Docker Hub ID)
DOCKER_USER="your-dockerhub-username"
IMAGE_NAME="google-flowx"
TAG="latest"

echo "=== Building Docker Image for Google-FlowX ==="
docker build -t $DOCKER_USER/$IMAGE_NAME:$TAG .

echo "=== Logging into Docker Hub ==="
docker login

echo "=== Pushing Image to Docker Hub ==="
docker push $DOCKER_USER/$IMAGE_NAME:$TAG

echo "=== SUCCESS: Published $DOCKER_USER/$IMAGE_NAME:$TAG to Docker Hub! ==="
