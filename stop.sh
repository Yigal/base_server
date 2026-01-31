#!/bin/bash

# Server shutdown script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: config.json not found"
    exit 1
fi

DOCKER_IMAGE=$(jq -r '.run_details.docker_image' "$CONFIG_FILE")
PID_FILE=$(jq -r '.run_details.pid_file' "$CONFIG_FILE")
CONTAINER_NAME=$(echo "$DOCKER_IMAGE" | cut -d: -f1 | tr '-' '_')_container

if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "Stopping container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" || true
    docker rm "$CONTAINER_NAME" || true
    echo "✓ Container stopped"
else
    echo "Container not running"
fi

# Remove PID file
if [ -f "$SCRIPT_DIR/$PID_FILE" ]; then
    rm -f "$SCRIPT_DIR/$PID_FILE"
fi

echo "✓ Server stopped"
