# Multi-Agent Architecture Security Analysis Platform

A distributed web application that leverages multiple AI agents to analyze software architectures and identify security vulnerabilities using the Strands framework.

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development (includes testing tools)
pip install -r requirements-dev.txt

# Run the coordinator
python -m src.coordinator.main

# Start the web interface
cd frontend && npm install && npm run dev
```

## Architecture

- **Agents**: Specialized security analysis agents
- **Coordinator**: Orchestrates agent workflows
- **Frontend**: Vue.js dashboard
- **Infrastructure**: AWS deployment configurations