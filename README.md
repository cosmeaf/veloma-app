# Veloma CRM Backend

A robust, modular Django-based authentication and security service designed for high-availability and security-conscious applications.

## 🚀 Overview

This platform provides a centralized authentication system featuring advanced security measures, including:
- **Modular Authentication:** Register, Login, Logout, and Profile management.
- **Security Layers:** Brute-force protection, Session limiting, and Account blocking.
- **Risk Assessment:** Real-time IP Intelligence, GeoIP lookups, and suspicious login detection.
- **Recovery Flows:** Secure Password Reset and OTP (One-Time Password) verification.
- **Audit Logging:** Comprehensive event tracking for all authentication attempts.

## 🛠 Tech Stack

- **Framework:** [Django 6.0](https://www.djangoproject.com/) & [Django REST Framework](https://www.django-rest-framework.org/)
- **Authentication:** [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- **Task Queue:** [Celery](https://docs.celeryq.dev/) with [Redis](https://redis.io/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Storage:** [S3 / MinIO](https://aws.amazon.com/s3/) (via `django-storages`)
- **Security:** [django-ipware](https://github.com/un33k/django-ipware), [GeoIP2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)

## 🏗 Architecture

The project follows a **Service-Oriented Architecture (SOA)** within Django:
- **Models:** Pure data definitions.
- **Serializers:** Request validation and data transformation.
- **Services:** All business logic is encapsulated here, making it reusable and testable.
- **DTOs (Data Transfer Objects):** Decouple internal models from external API contracts.
- **Middleware:** Injected context for auditing and session validation.

## 📂 Project Structure

```text
├── authentication/      # Core auth logic (Models, Services, Views)
│   ├── dto/             # Data Transfer Objects
│   ├── services/        # Business logic layer
│   └── views/           # API Endpoints
├── core/                # Project configuration (settings, urls, asgi/wsgi)
├── services/            # Shared utilities (Email, Auth helpers, Middleware)
├── templates/           # Email and HTML templates
├── tests/               # Pytest suite
└── manage.py            # Django management script
```

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.12+
- Redis (running on port 6380 by default)
- PostgreSQL

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory and populate it based on `core/settings.py` requirements (SECRET_KEY, DB credentials, etc.).

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

## 🏃 Running the Application

### 1. Django Server
```bash
python manage.py runserver 0.0.0.0:7000
```

### 2. Celery Worker (Email & Tasks)
```bash
celery -A core worker -l info -Q emails,celery
```

### 3. Celery Beat (Scheduled Tasks)
```bash
celery -A core beat -l info
```

Alternatively, use the provided management script:
```bash
./start_manager.sh start
```

## 🧪 Testing

Run the test suite using `pytest`:
```bash
pytest
```

## 🔒 Security Audit Notes (Current Status)
- **Middleware:** Synchronous GeoIP lookups are enabled.
- **OTP:** Uses 6-digit numeric codes.
- **Logs:** Hardcoded to `/var/log/veloma/` (requires proper permissions).

---
*Developed by the Veloma Engineering Team.*
