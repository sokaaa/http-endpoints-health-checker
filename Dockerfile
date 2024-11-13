# Use an official Python runtime as the base image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the environment variable to disable output buffering
ENV PYTHONUNBUFFERED=1

# Default command to run the Python script, argument will be passed at runtime
ENTRYPOINT ["python3", "monitor.py"]
