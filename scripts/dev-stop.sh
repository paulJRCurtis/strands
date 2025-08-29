#!/bin/bash

echo "Stopping Strands Security Analysis Platform..."

# Stop Python coordinator processes
echo "Stopping coordinator..."
pkill -f "python -m src.coordinator.main"

# Stop frontend development server
echo "Stopping frontend..."
pkill -f "npm run dev"
pkill -f "vite"

# Wait a moment for processes to terminate
sleep 2

# Check if processes are still running and force kill if necessary
COORD_PID=$(pgrep -f "python -m src.coordinator.main")
if [ ! -z "$COORD_PID" ]; then
    echo "Force stopping coordinator..."
    kill -9 $COORD_PID
fi

FRONTEND_PID=$(pgrep -f "vite")
if [ ! -z "$FRONTEND_PID" ]; then
    echo "Force stopping frontend..."
    kill -9 $FRONTEND_PID
fi

echo "Development environment stopped."
echo "Ports 8000 and 3000 are now available."