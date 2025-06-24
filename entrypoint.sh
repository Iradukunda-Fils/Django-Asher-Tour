#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."

# Wait until PostgreSQL is ready
until nc -z "$POSTGRESQL_HOST" "$POSTGRESQL_PORT"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done


echo "PostgreSQL is up - continuing..."

# Apply database migrations

echo "Applying database migrations..."
python manage.py makemigrations system_db
python manage.py makemigrations
python manage.py migrate
# python manage.py makemigrations --merge

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if not exists
echo "Creating default superuser if not exists..."

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="${DJANGO_SUPERUSER_EMAIL}").exists():
    print("Creating superuser ${DJANGO_SUPERUSER_EMAIL}")
    User.objects.create_superuser(
        email="${DJANGO_SUPERUSER_EMAIL}",
        first_name="${DJANGO_SUPERUSER_FIRSTNAME}",
        last_name="${DJANGO_SUPERUSER_LASTNAME}",
        phone="${DJANGO_SUPERUSER_PHONE}",
        country="${DJANGO_SUPERUSER_COUNTRY}",
        password="${DJANGO_SUPERUSER_PASSWORD}",
    )
else:
    print("Superuser already exists.")
END

# Run default CMD (like gunicorn)
exec "$@"
