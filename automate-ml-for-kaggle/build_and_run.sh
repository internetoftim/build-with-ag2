#!/bin/bash

# Exit on error
set -e

# Display header
echo "=========================================================="
echo "🐳 ML Agent Docker Environment Builder"
echo "=========================================================="

# Build the Docker image
echo "Building Docker image..."
docker build -t ml-agent:latest .

echo "Docker image built successfully!"
echo ""
echo "You can run the container using either:"
echo ""
echo "1. Docker directly:"
echo "   docker run --rm -v $(pwd):/app ml-agent:latest train_file_by_agent.py"
echo ""
echo "2. Docker Compose:"
echo "   docker-compose up"
echo ""
echo "3. For development with live code changes:"
echo "   docker-compose up --build"
echo ""
echo "To run a different script:"
echo "   docker run --rm -v $(pwd):/app ml-agent:latest your_script.py"
echo ""
echo "To start an interactive shell:"
echo "   docker run --rm -it -v $(pwd):/app ml-agent:latest /bin/bash"
echo "=========================================================="
