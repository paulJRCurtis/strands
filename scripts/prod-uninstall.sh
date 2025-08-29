#!/bin/bash

echo "🗑️  Uninstalling Strands Security Analysis Platform (Production)..."

# Stop and remove containers
echo "Stopping production containers..."
docker-compose -f docker-compose.prod.yml down --volumes --remove-orphans

# Remove Docker images
echo "Removing Docker images..."
docker rmi strands-coordinator:latest 2>/dev/null || true
docker rmi strands-frontend:latest 2>/dev/null || true
docker rmi strands-security-platform:latest 2>/dev/null || true

# Remove all tagged versions
echo "Removing tagged images..."
docker images | grep strands | awk '{print $1":"$2}' | xargs -r docker rmi 2>/dev/null || true

# Remove Docker networks
echo "Removing Docker networks..."
docker network rm strands_strands-network 2>/dev/null || true

# Clean up Docker system
echo "Cleaning up Docker system..."
docker system prune -f --volumes

# Remove application data
echo "Removing application data..."
rm -rf test-results/ 2>/dev/null || true
rm -rf frontend/test-results/ 2>/dev/null || true
rm -rf logs/ 2>/dev/null || true

# Remove build artifacts
echo "Removing build artifacts..."
rm -rf frontend/dist/ 2>/dev/null || true
rm -rf frontend/node_modules/ 2>/dev/null || true

echo ""
echo "✅ Strands Security Analysis Platform completely uninstalled!"
echo ""
echo "Removed:"
echo "- All Docker containers and images"
echo "- Docker networks and volumes"
echo "- Application data and logs"
echo "- Build artifacts"
echo ""
echo "Ports 8000 and 3000 are now available."