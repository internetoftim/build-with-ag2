#!/bin/bash

# Excel-Doc Agent Setup Script
# This script sets up a Python virtual environment and installs all required dependencies

echo "Setting up Excel-Doc Agent environment..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -U autogen-agentchat
pip install -r requirements.txt

# Create workspace directories
echo "Creating workspace directories..."
mkdir -p workspace/jupyter_output

# Create workspace directory if it doesn't exist
echo "Creating workspace directory..."
mkdir -p workspace

echo "Setup complete! You can now run the Excel-Doc Agent with:"
echo "source venv/bin/activate && python main.py"
