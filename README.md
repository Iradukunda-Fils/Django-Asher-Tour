# 🚀 Asher Safaris – Tour Company Platform

This is a Django-based web platform built for **Asher Safaris**, a travel and tourism company.  
It allows the company to manage tour packages, handle bookings, and showcase destinations with integrated media content.

---

## 🧭 Project Overview

**Client**: Asher Safaris  
**Purpose**: To provide a modern, scalable, and reliable backend for a tour booking and management platform using:

- Django + PostgreSQL for the backend logic and database
- Gunicorn as the WSGI server
- Nginx as the reverse proxy (production-ready)
- Docker for containerized CI/CD-friendly deployment

---

## ⚙️ System Architecture (CI/CD Ready)

User ──> NGINX ──> Gunicorn ──> Django ──> PostgreSQL
│
Static/Media via Docker Volumes



- ✅ Auto-handled database migrations
- ✅ Static/media persistence via Docker volumes
- ✅ Superuser is created via environment variables
- ✅ Easily scalable with Docker Compose

---

## 📦 Requirements

- Docker
- Docker Compose

---

## 🔧 Setup & Deployment (1 Command)

### 1. Prepare `.env`

Create a `.env` file at the root with:

```ini
SECRET_KEY=django-insecure-hhr)m38w)*j4oipcuy3!vd$*jz@8t)4gef0j+6+4o9x)9tm$=ohs
DEBUG=False
ALLOWED_HOSTS=*

POSTGRES_DB=asher_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
POSTGRESQL_HOST=db
POSTGRESQL_PORT=5432

DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_FIRSTNAME=Fadmin
DJANGO_SUPERUSER_LASTNAME=Ladmin
DJANGO_SUPERUSER_PHONE="+250781234567"
DJANGO_SUPERUSER_COUNTRY="RW"
DJANGO_SUPERUSER_PASSWORD="adminpass123"

2. Run Everything

---
docker compose up --build
---


Runs all services: web, db, nginx

Collects static files

Applies migrations

Creates a superuser

No manual steps needed.

🔍 Accessing the System
App URL: http://localhost

Admin Panel: http://localhost/admin

Email: admin@example.com

Password: adminpass123

🗃️ Volumes
static_volume → /app/staticfiles

media_volume → /app/Asher_Media

.:/app → for live code updates

📁 Tech Stack
Component	Tool
Backend	Django
Database	PostgreSQL
WSGI Server	Gunicorn
Proxy	Nginx
DevOps	Docker Compose

✅ Summary
This is a ready-to-deploy Django platform for Asher Safaris, optimized for CI/CD workflows, containerized deployment, and simple developer handoff.

You can deploy, scale, and test the platform using Docker Compose, with no extra configuration or manual setup.


© Developed for Asher Safaris by [Iradukunda Fils]


---

Would you like to also generate the production-ready `nginx.conf`, `Dockerfile`, or `docker-compose.yml` content to match this deployment?


---