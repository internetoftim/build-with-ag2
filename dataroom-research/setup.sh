#!/bin/bash

echo "=== DataRoom Research: DeepResearchAgent + GoogleDrive Setup ==="
echo "This script will set up the DataRoom Research environment"

# Create virtual environment
echo "\n=== Creating Python virtual environment ==="
python -m venv venv

# Activate virtual environment
echo "=== Activating virtual environment ==="
source venv/bin/activate

# Install Python dependencies
echo "\n=== Installing Python dependencies ==="
pip install -r requirements.txt

# Install Playwright browsers (required for web research)
echo "\n=== Installing Playwright browsers for web research ==="
python -m playwright install

# Check for OAI_CONFIG_LIST
echo "\n=== Checking for API configuration ==="
if [ ! -f "OAI_CONFIG_LIST" ]; then
  echo "Creating OAI_CONFIG_LIST from sample template"
  cp OAI_CONFIG_LIST_sample OAI_CONFIG_LIST
  echo "⚠️  Please edit OAI_CONFIG_LIST to add your OpenAI API key"
else
  echo "OAI_CONFIG_LIST already exists"
fi

# Check for Google Drive credentials
if [ ! -f "credentials.json" ]; then
  echo "\n⚠️  No Google Drive credentials.json found"
  echo "To use Google Drive features, download OAuth credentials from Google Cloud Console"
  echo "and save as 'credentials.json' in this directory"
else
  echo "\n✅ Google Drive credentials.json found"
fi

# Offer to install Ollama
echo "\n=== Local LLM Setup (Optional) ==="
echo "Would you like to set up Ollama for local LLM support? (y/n)"
read -r setup_ollama

if [ "$setup_ollama" = "y" ] || [ "$setup_ollama" = "Y" ]; then
  echo "Please visit https://ollama.ai/download and install Ollama for your system"
  echo "After installation, run: ollama pull deepseek-r1"
  
  # Check if OLLAMA_CONFIG_LIST exists
  if [ ! -f "OLLAMA_CONFIG_LIST" ]; then
    echo "Creating OLLAMA_CONFIG_LIST from sample template"
    cp OLLAMA_CONFIG_LIST_sample OLLAMA_CONFIG_LIST
  fi
fi

echo "\n✅ Setup completed successfully!"
echo "Activate the virtual environment with: source venv/bin/activate"
echo "Run the application with: python main.py"
echo "For options, try: python main.py --help"

