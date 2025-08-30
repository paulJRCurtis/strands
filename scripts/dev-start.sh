#!/bin/bash



# Activate venv
if [ ! -d ".venv" ]; then
	echo "Python virtual environment not found. Please create it first."
	exit 1
fi
source .venv/bin/activate

# Check if .venv is active
VENV_PATH="$(pwd)/.venv"
if [[ "$(which python)" != "$VENV_PATH/bin/python"* ]] || [[ "$(which pip)" != "$VENV_PATH/bin/pip"* ]]; then
	echo "Error: .venv is not activated properly."
	exit 1
fi

# Check and install Python dependencies
REQ_FILE="requirements.txt"
if [ -f "$REQ_FILE" ]; then
	echo "Checking and installing Python dependencies from $REQ_FILE..."
	pip install --upgrade pip setuptools wheel
	pip install -r "$REQ_FILE"
else
	echo "No requirements.txt found. Skipping Python dependency installation."
fi

# Start coordinator
echo "Starting coordinator..."
python -m src.coordinator.main &
COORDINATOR_PID=$!

# Wait for coordinator to start
sleep 3


# Start frontend
echo "Starting frontend..."
cd frontend
echo "Checking and installing Node.js dependencies..."
npm install
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