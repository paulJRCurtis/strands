#!/bin/bash

echo "🗑️  Uninstalling Strands Security Analysis Platform (Test Environment)..."

# Stop and remove test containers
echo "Stopping test containers..."
docker-compose -f docker-compose.test.yml down --volumes --remove-orphans 2>/dev/null || true

# Remove test Docker images
echo "Removing test Docker images..."
docker rmi strands-coordinator:latest 2>/dev/null || true
docker rmi node:18-alpine 2>/dev/null || true
docker rmi mcr.microsoft.com/playwright:v1.40.0-focal 2>/dev/null || true

# Remove Docker networks
echo "Removing Docker networks..."
docker network rm strands_test-network 2>/dev/null || true

# Clean up test data
echo "Removing test data..."
rm -rf test-results/ 2>/dev/null || true
rm -rf frontend/test-results/ 2>/dev/null || true

# Remove test artifacts
echo "Removing test artifacts..."
rm -rf frontend/playwright-report/ 2>/dev/null || true
rm -rf .pytest_cache/ 2>/dev/null || true
rm -rf frontend/.nyc_output/ 2>/dev/null || true
rm -rf frontend/coverage/ 2>/dev/null || true

# Remove test-specific files
echo "Removing test files..."
rm -f *.xml 2>/dev/null || true
rm -f coverage.xml 2>/dev/null || true
rm -f test-results.xml 2>/dev/null || true

echo ""
echo "✅ Test environment completely uninstalled!"
echo ""
echo "Removed:"
echo "- All test containers and images"
echo "- Test networks and volumes"
echo "- Test results and reports"
echo "- Coverage data"
echo "- Playwright artifacts"
echo ""
echo "Test environment is now clean."