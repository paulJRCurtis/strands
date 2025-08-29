#!/bin/bash

echo "Starting Strands Security Analysis Platform (Production Mode)..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed."
    exit 1
fi

# Build and start production containers
echo "Building and starting production containers..."
docker-compose -f docker-compose.prod.yml up --build -d

# Wait for services to start
echo "Waiting for services to initialize..."
sleep 10

# Check if containers are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo ""
    echo "✅ Production environment started successfully!"
    echo ""
    echo "Services available at:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000"
    echo "- API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
    echo "To stop: ./scripts/prod-stop.sh"
else
    echo "❌ Failed to start production environment"
    echo "Check logs: docker-compose -f docker-compose.dev.yml logs"
    exit 1
fi