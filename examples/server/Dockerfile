# Simple Dockerfile for the FastAPI server (CPU-only)
# For GPU support, use an NVIDIA CUDA base image and install a matching torch build.

FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Optional: install audiocraft from GitHub (comment/uncomment as needed)
# Installing audiocraft here may require a matching torch wheel for CUDA/CPU and can be large.
# RUN pip install git+https://github.com/facebookresearch/audiocraft.git

COPY app.py /app/app.py

ENV MODEL_NAME=medium

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
