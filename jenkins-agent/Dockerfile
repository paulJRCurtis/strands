# Strands Security Analysis Platform - Jenkins Agent
# This Dockerfile creates a Jenkins agent with all tools required for the
# Strands CI/CD pipeline including Docker, Python, Node.js, and security tools.

FROM jenkins/inbound-agent:latest

# Switch to root for installations
USER root

# Update package list and install system dependencies
RUN apt-get update && apt-get install -y \
    # Docker and Docker Compose
    docker.io \
    docker-compose \
    # Python and pip
    python3 \
    python3-pip \
    # Node.js and npm
    nodejs \
    npm \
    # Utility tools
    curl \
    wget \
    sed \
    git \
    unzip \
    # Build tools
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python testing and security tools
RUN pip3 install --no-cache-dir \
    pytest \
    pytest-cov \
    bandit \
    coverage --break-system-packages

# Add to OWASP Dependency Check
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://github.com/jeremylong/DependencyCheck/releases/download/v8.4.0/dependency-check-8.4.0-release.zip && \
    unzip dependency-check-8.4.0-release.zip -d /opt && \
    ln -s /opt/dependency-check/bin/dependency-check.sh /usr/local/bin/dependency-check


# Install Trivy security scanner
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Install SonarQube scanner
RUN wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip \
    && unzip sonar-scanner-cli-4.8.0.2856-linux.zip -d /opt/ \
    && ln -s /opt/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner \
    && rm sonar-scanner-cli-4.8.0.2856-linux.zip

# Add jenkins user to docker group for Docker socket access
RUN usermod -aG docker jenkins

# Create workspace directory
RUN mkdir -p /home/jenkins/agent && chown jenkins:jenkins /home/jenkins/agent

# Copy verification script into agent workspace
COPY verify-agent.sh /home/jenkins/agent/verify-agent.sh
RUN chmod +x /home/jenkins/agent/verify-agent.sh

# Switch back to jenkins user
USER jenkins

# Set working directory
WORKDIR /home/jenkins/agent

# Verify installations
RUN docker --version || echo "Docker not available (requires socket mount)" \
    && docker-compose --version \
    && python3 --version \
    && pip3 --version \
    && node --version \
    && npm --version \
    && pytest --version \
    && bandit --version \
    && trivy --version \
    && sonar-scanner --version

# Set environment variables
ENV DOCKER_HOST=unix:///var/run/docker.sock
ENV PYTHONPATH=/home/jenkins/agent
ENV NODE_ENV=development

# Health check to verify agent is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080 || exit 1
