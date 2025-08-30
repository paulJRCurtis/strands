# Strands Security Analysis Platform - Backend Coordinator
# This Dockerfile builds the Python FastAPI backend service that orchestrates
# security analysis using multiple AI agents. Used in production, development,
# and test environments.

# Use Python 3.11 slim base image for smaller footprint
FROM python:3.11-slim

# Set working directory for the application
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code containing agents and coordinator
COPY ../src/ ./src/

# Expose port 8000 for FastAPI application
EXPOSE 8000

# Set Python path to include app directory
ENV PYTHONPATH=/app

# Start the FastAPI coordinator service
CMD ["python", "-m", "src.coordinator.main"]