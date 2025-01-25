# Use a lightweight Python base image
FROM python:3.11-slim

# Set environment variables to avoid .pyc files and unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    traceroute \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY /traceroute_history/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port used by the web server (if applicable)
EXPOSE 8000

# Default command to run the application
CMD ["python", "traceroute_history.py"]
