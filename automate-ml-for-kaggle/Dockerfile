FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required for certain Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY docker_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r docker_requirements.txt

# Copy the current directory contents into the container at /app
# For development, this can be mounted as a volume instead
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Command to run when the container starts
ENTRYPOINT ["python"]
CMD ["train_file_by_agent.py"]
