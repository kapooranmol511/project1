# Use the official Python image from the Docker Hub
FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code into the container
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
