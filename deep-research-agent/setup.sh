#!/bin/bash

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

echo "Setup completed successfully. Activate the virtual environment with 'source venv/bin/activate'"
