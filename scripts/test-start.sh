#!/bin/bash

echo "Starting containerized test environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Run tests in containers
echo "Running backend tests..."
docker-compose -f docker-compose.test.yml run --rm test-coordinator

echo "Running frontend tests..."
docker-compose -f docker-compose.test.yml run --rm test-frontend

echo "Running E2E tests..."
docker-compose -f docker-compose.test.yml run --rm e2e-tests

# Clean up
echo "Cleaning up test containers..."
docker-compose -f docker-compose.test.yml down

echo "✅ All tests completed!"
echo ""
echo "Test results available in:"
echo "- Backend: test-results/"
echo "- Frontend: frontend/test-results/"