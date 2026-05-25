#!/bin/bash

# StageReady — This script was done partly with Artificial Intelligence to make it easier to run the course.

echo "--- StageReady acting course starting ---"

if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed. Please install it from python.org"
    exit
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies (this may take a minute)..."
source venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating a default .env file..."
    echo "SECRET_KEY=dev-secret-key-12345" > .env
    echo "GEMINI_API_KEY=your_key_here" >> .env
fi

echo "Launching StageReady at http://127.0.0.1:5001"
echo "Press Ctrl+C to stop the server."
python3 app.py
