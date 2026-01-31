#!/bin/bash

# Server startup script
# Requirements:
#   - config.json must exist in the same directory
#   - Docker must be installed and running

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

# Check config.json exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: config.json not found in $SCRIPT_DIR"
    exit 1
fi

# Extract configuration from config.json
DOCKER_IMAGE=$(jq -r '.run_details.docker_image' "$CONFIG_FILE")
ROOT_PORT=$(jq -r '.run_details.root_port' "$CONFIG_FILE")
STORAGE_FOLDER=$(jq -r '.run_details.local_storage_folder' "$CONFIG_FILE")
PID_FILE=$(jq -r '.run_details.pid_file' "$CONFIG_FILE")
CONTAINER_NAME=$(echo "$DOCKER_IMAGE" | cut -d: -f1 | tr '-' '_')_container

# Create storage folder if it doesn't exist
mkdir -p "$SCRIPT_DIR/$STORAGE_FOLDER"

# Check if server is already running
if [ -f "$SCRIPT_DIR/$PID_FILE" ]; then
    echo "Server appears to be running. Stopping first..."
    bash "$SCRIPT_DIR/stop.sh" || true
fi

# Check if port is still in use
if lsof -i ":$ROOT_PORT" > /dev/null 2>&1; then
    echo "ERROR: Port $ROOT_PORT is still in use"
    exit 1
fi

# Build Docker image
echo "Building Docker image: $DOCKER_IMAGE"
docker build -t "$DOCKER_IMAGE" "$SCRIPT_DIR"

# Run Docker container
echo "Starting server on port $ROOT_PORT..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$ROOT_PORT:8000" \
    -p "$((ROOT_PORT + 1)):8001" \
    -v "$SCRIPT_DIR/$STORAGE_FOLDER:/app/storage" \
    "$DOCKER_IMAGE"

# Wait for container to start
sleep 3

# Get container PID and save it
DOCKER_PID=$(docker inspect -f '{{.State.Pid}}' "$CONTAINER_NAME")
echo "$DOCKER_PID" > "$SCRIPT_DIR/$PID_FILE"

echo "✓ Server started successfully"
echo "  Dashboard: http://localhost:$ROOT_PORT/ui/"
echo "  API: http://localhost:$((ROOT_PORT + 1))/api/"
echo "  PID: $DOCKER_PID"

# Run BIST tests
echo "Running BIST tests..."
docker exec "$CONTAINER_NAME" python -m pytest tests/bist_runner.py -v || true
