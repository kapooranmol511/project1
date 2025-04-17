# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install dependencies for Poppler
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*
    # poppler-utils \
    # tesseract-ocr \
    # && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# **Download the spaCy model**
RUN python -m spacy download en_core_web_sm

# Copy the FastAPI app code into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
