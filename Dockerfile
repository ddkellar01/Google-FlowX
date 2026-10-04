# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for OpenCV, FFmpeg, and ML libraries
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install project python dependencies
RUN pip install --no-cache-dir \
    numpy \
    opencv-python-headless \
    tensorflow \
    torch \
    torchvision \
    torchaudio \
    vertexai \
    google-cloud-aiplatform \
    google-cloud-storage \
    google-cloud-logging \
    google-cloud-container \
    google-cloud-monitoring \
    google-cloud-translate \
    fastapi \
    uvicorn \
    requests \
    redis \
    gitpython \
    pynvml \
    sentence-transformers \
    scikit-learn \
    ffmpeg-python

# Copy the entire project structure into the container
COPY . /app

# Expose API port for the Gateway
EXPOSE 8000

# Default command to start the API gateway / orchestration router
CMD ["uvicorn", "orchestrator.api_gateway:app", "--host", "0.0.0.0", "--port", "8000"]
