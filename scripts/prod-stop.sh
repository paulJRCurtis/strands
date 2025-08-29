#!/bin/bash

echo "Stopping Strands Security Analysis Platform (Production Mode)..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed."
    exit 1
fi

# Stop and remove containers
echo "Stopping production containers..."
docker-compose -f docker-compose.prod.yml down

# Remove unused images and volumes (optional cleanup)
echo "Cleaning up unused resources..."
docker system prune -f --volumes

# Verify containers are stopped
if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo ""
    echo "✅ Production environment stopped successfully!"
    echo ""
    echo "All containers have been stopped and removed."
    echo "Ports 8000 and 3000 are now available."
else
    echo "❌ Some containers may still be running"
    echo "Check status: docker-compose -f docker-compose.prod.yml ps"
fi