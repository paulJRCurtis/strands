#!/bin/bash

echo "🗑️  Uninstalling Strands Security Analysis Platform (Development)..."

# Stop development processes
echo "Stopping development processes..."
pkill -f "python -m src.coordinator.main" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true

# Stop and remove dev containers
echo "Stopping development containers..."
docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true

# Remove Docker images
echo "Removing Docker images..."
docker rmi strands-coordinator:latest 2>/dev/null || true
docker rmi node:18-alpine 2>/dev/null || true

# Remove Docker networks
echo "Removing Docker networks..."
docker network rm strands_strands-network 2>/dev/null || true

# Clean up development data
echo "Removing development data..."
rm -rf test-results/ 2>/dev/null || true
rm -rf frontend/test-results/ 2>/dev/null || true
rm -rf logs/ 2>/dev/null || true
rm -rf __pycache__/ 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Remove frontend development artifacts
echo "Removing frontend artifacts..."
rm -rf frontend/node_modules/ 2>/dev/null || true
rm -rf frontend/dist/ 2>/dev/null || true

echo ""
echo "✅ Development environment completely uninstalled!"
echo ""
echo "Removed:"
echo "- All development processes"
echo "- Docker containers and networks"
echo "- Development data and logs"
echo "- Python cache files"
echo "- Frontend dependencies"
echo ""
echo "Ports 8000 and 3000 are now available."