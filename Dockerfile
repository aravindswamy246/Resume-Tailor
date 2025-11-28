# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expose port
EXPOSE 8000

# Run the application with uvicorn
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]