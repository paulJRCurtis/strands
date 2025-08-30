#!/bin/bash

# Strands Security Analysis Platform - Environment Setup
# Sets environment variables for local development

export DEBUG=true
export LOG_LEVEL=DEBUG
export NODE_ENV=development
export API_BASE_URL=http://localhost:8000
export FRONTEND_URL=http://localhost:3000
export CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

echo "Environment variables set for local development:"
echo "DEBUG=$DEBUG"
echo "LOG_LEVEL=$LOG_LEVEL"
echo "NODE_ENV=$NODE_ENV"
echo "API_BASE_URL=$API_BASE_URL"
echo "FRONTEND_URL=$FRONTEND_URL"