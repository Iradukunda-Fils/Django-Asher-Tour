# Build stage
FROM python:3.13.3-bookworm AS build

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y gcc libpq-dev libffi-dev libssl-dev build-essential && \
    pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

COPY . .

RUN find /app -type d -name "__pycache__" -exec rm -r {} + && \
    find /app -name "*.pyc" -delete


# Final slim image
FROM python:3.13.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY --from=build /app /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx curl netcat-openbsd && \
    rm /etc/nginx/sites-enabled/default && \
    mkdir -p /run/nginx && \
    chmod +x /app/entrypoint.sh && \
    mv /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

EXPOSE 80
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["/bin/sh", "-c", "nginx && gunicorn Asher_tour.wsgi:application --bind 0.0.0.0:8000"]
