FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including postgresql-client for pg_isready
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (will be overridden by volume mount in dev)
COPY . .

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Default command (overridden by docker-compose)
CMD ["celery", "-A", "src.celery_app", "worker", "-l", "info"]
