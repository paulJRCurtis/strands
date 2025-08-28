#!/bin/bash

# Start coordinator
echo "Starting coordinator..."
cd /Users/paucurt/projects/strands
python -m src.coordinator.main &
COORDINATOR_PID=$!

# Wait for coordinator to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "Services started:"
echo "- Coordinator: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $COORDINATOR_PID $FRONTEND_PID; exit" INT
wait