# Upgrade to Python 3.11 to satisfy updated ML dependencies
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by your packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project structure into the container
COPY . .

# Add your startup command here if needed (e.g., CMD ["python", "app.py"])
