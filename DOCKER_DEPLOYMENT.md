# Docker Deployment Guide

## Quick Start

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f coordinator
```

## Architecture

- **coordinator**: Python FastAPI backend (port 8000)
- **frontend**: Vue.js + Nginx (port 3000)
- **redis**: Agent coordination and caching
- **nginx**: Production load balancer (ports 80/443)

## Files Created

- `docker-compose.yml` - Development environment
- `docker-compose.prod.yml` - Production environment
- `frontend/Dockerfile` - Multi-stage Vue.js build
- `frontend/nginx.conf` - Frontend proxy configuration
- `.dockerignore` - Build optimization

## Production Deployment

```bash
# Start production stack
docker-compose -f docker-compose.prod.yml up -d

# Scale coordinators
docker-compose up --scale coordinator=3

# Update single service
docker-compose up -d --no-deps coordinator
```

## Environment Configuration

Create `.env` file:
```bash
REDIS_URL=redis://redis:6379
API_PORT=8000
FRONTEND_PORT=3000
ENVIRONMENT=production
```

## Key Features

- Multi-stage builds for optimized images
- Service isolation and networking
- Redis persistence
- Development/production separation
- Health checks and restart policies
- SSL-ready Nginx configuration

## Monitoring

```bash
# Service status
docker-compose ps

# Resource usage
docker stats

# Container logs
docker-compose logs -f [service-name]
```