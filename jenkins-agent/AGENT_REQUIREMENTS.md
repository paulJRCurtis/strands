# Jenkins Docker Agent Requirements for Strands Pipeline

## Overview

This document outlines the specific requirements for the Docker agent to run the Strands Security Analysis Platform CI/CD pipeline.

## Docker Agent Requirements

### 1. Base Image & Runtime

The Jenkins agent must include all necessary tools for building, testing, and deploying the Strands platform.

### 2. Volume Mounts (Critical)

```yaml
# docker-compose.yml for Jenkins agent
services:
  jenkins-agent:
    image: strands-jenkins-agent
    volumes:
      # Essential: Docker socket for Docker-in-Docker
      - /var/run/docker.sock:/var/run/docker.sock
      # Optional: Docker binary (if not in image)
      - /usr/bin/docker:/usr/bin/docker:ro
      # Workspace persistence
      - jenkins-workspace:/home/jenkins/agent
```

### 3. Required Tools & Versions

| Tool | Version | Purpose |
|------|---------|---------|
| **Docker** | 20.10+ | Container builds and deployment |
| **Docker Compose** | 2.0+ | Multi-container orchestration |
| **Python** | 3.8+ | Backend testing and SAST |
| **Node.js** | 16+ | Frontend builds and testing |
| **npm** | 8+ | Frontend package management |
| **curl** | Any | Health checks and API calls |
| **sed** | Any | File manipulation for deployments |
| **git** | Any | Source code checkout |

### 4. Security Tools

Required for SAST and container security scanning:
- **bandit** - Python security analysis
- **trivy** - Container vulnerability scanning
- **pytest** - Python testing framework

### 5. Network Configuration

```yaml
# Agent needs access to:
networks:
  - jenkins-network  # Communication with Jenkins master
  - default         # Internet access for downloads
```

### 6. Environment Variables

```bash
# Required environment variables
DOCKER_HOST=unix:///var/run/docker.sock
JENKINS_URL=http://jenkins-master:8080
JENKINS_SECRET=<agent-secret>
JENKINS_AGENT_NAME=docker-agent
```

### 7. Resource Requirements

```yaml
# Minimum resources
deploy:
  resources:
    limits:
      memory: 4G
      cpus: '2'
    reservations:
      memory: 2G
      cpus: '1'
```

### 8. Permissions

```bash
# Agent user needs Docker group membership
usermod -aG docker jenkins

# Or run with appropriate permissions
docker run --group-add $(getent group docker | cut -d: -f3) ...
```

### 9. Complete Agent Configuration

```yaml
# docker-compose.yml for Jenkins setup
version: '3.8'
services:
  jenkins-agent:
    build: 
      context: .
      dockerfile: Dockerfile
    environment:
      - JENKINS_URL=http://jenkins:8080
      - JENKINS_SECRET=${JENKINS_SECRET}
      - JENKINS_AGENT_NAME=docker-agent
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - jenkins-workspace:/home/jenkins/agent
    networks:
      - jenkins-network
    depends_on:
      - jenkins

volumes:
  jenkins-workspace:

networks:
  jenkins-network:
    driver: bridge
```

### 10. Verification Script

```bash
#!/bin/bash
# verify-agent.sh - Run inside agent to verify setup

echo "Checking Docker..."
docker --version && docker ps

echo "Checking Docker Compose..."
docker-compose --version

echo "Checking Python tools..."
python3 --version && pip3 list | grep -E "(pytest|bandit)"

echo "Checking Node.js..."
node --version && npm --version

echo "Checking security tools..."
trivy --version

echo "Checking network connectivity..."
curl -s http://jenkins:8080 > /dev/null && echo "Jenkins accessible"

echo "Agent verification complete!"
```

## Key Points

- **Docker socket mount is critical** - Without it, no Docker commands work
- **Tool versions matter** - Ensure compatibility with your codebase
- **Security tools required** - For SAST and container scanning stages
- **Network access needed** - For registry pushes and health checks
- **Sufficient resources** - Building containers is resource-intensive

## Usage

1. Build the Docker image: `docker build -t strands-jenkins-agent .`
2. Configure Jenkins to use this agent
3. Run verification script to ensure all tools are available
4. Execute Strands pipeline

This configuration provides everything needed to run the Strands pipeline successfully.