# Use slim version of Python image
FROM python:3.13.3-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Pre-install dependencies to improve layer caching
COPY requirements.txt .

# Install system & Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
        netcat-openbsd \
        libffi-dev \
        libssl-dev \
        build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project code
COPY . .

# Ensure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose port (internal only; nginx will proxy this)
EXPOSE 8000

# Set entrypoint to wait for DB & create superuser
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command: run gunicorn server
CMD ["gunicorn", "Asher_tour.wsgi:application", "--bind", "0.0.0.0:8000"]
