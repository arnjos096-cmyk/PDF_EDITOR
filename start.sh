#!/bin/bash

# AI PDF Commander - Startup Script

echo "========================================="
echo "   AI PDF Commander"
echo "   Chat-based PDF Editor"
echo "========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found."
    exit 1
fi

# Check for g++
if ! command -v g++ &> /dev/null; then
    echo "Error: g++ compiler is required but not found."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Build C++ backend
echo "Building C++ backend..."
cd backend
make clean > /dev/null 2>&1
make
if [ $? -ne 0 ]; then
    echo "Error: Failed to build C++ backend"
    exit 1
fi
cd ..

echo ""
echo "✅ Build successful!"
echo ""
echo "Starting server..."
echo "Access the application at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask server
python3 api/server.py
