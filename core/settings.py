"""
Django settings for core project.
"""
import os
import sys
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = "/var/log/veloma"
os.makedirs(LOG_DIR, exist_ok=True)
sys.path.append("/opt/ipintel")

if "pytest" in sys.modules:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="127.0.0.1,localhost")

APPEND_SLASH = False
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DJANGO_ENV = config("DJANGO_ENV", default="development")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "storages",
    "authentication",
    "services",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "services.middleware.request_context.RequestContextMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [os.path.join(BASE_DIR, 'templates')],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/veloma-crm/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = "/var/www/veloma-crm/media/"

GEOIP_PATH = config("GEOIP_PATH", default="/opt/ipintel/geoip")

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv(), default="")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", cast=bool)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config("SECURE_CONTENT_TYPE_NOSNIFF", cast=bool)
SECURE_BROWSER_XSS_FILTER = config("SECURE_BROWSER_XSS_FILTER", cast=bool)
SECURE_REFERRER_POLICY = config("SECURE_REFERRER_POLICY")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_LIFETIME", cast=int, default=60)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_LIFETIME", cast=int, default=7)
    ),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REDIS_URL = config("REDIS_URL", default="redis://127.0.0.1:6380/0")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", cast=bool)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv(), default="")

EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", cast=int, default=30)

PUBLIC_BASE_URL = config("PUBLIC_BASE_URL")
FRONTEND_BASE_URL = config("FRONTEND_BASE_URL")
AUTH_RESET_PASSWORD_PATH = config("AUTH_RESET_PASSWORD_PATH")

LOGIN_ALERT_ENABLED = config("LOGIN_ALERT_ENABLED", cast=bool)
LOGIN_ALERT_GEOLOOKUP_ENABLED = config("LOGIN_ALERT_GEOLOOKUP_ENABLED", cast=bool)
LOGIN_ALERT_GEOLOOKUP_URL = config("LOGIN_ALERT_GEOLOOKUP_URL")
LOGIN_ALERT_GEOLOOKUP_TIMEOUT = config("LOGIN_ALERT_GEOLOOKUP_TIMEOUT", cast=int)

USER_PROFILE_ENCRYPTION_KEY = config("USER_PROFILE_ENCRYPTION_KEY")

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
AWS_S3_SIGNATURE_VERSION = config("AWS_S3_SIGNATURE_VERSION")
AWS_S3_ADDRESSING_STYLE = config("AWS_S3_ADDRESSING_STYLE")

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_DIR}/django.log",
            "maxBytes": 20 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "standard",
        },
        "auth_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_DIR}/auth.log",
            "maxBytes": 20 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "standard",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{LOG_DIR}/error.log",
            "maxBytes": 20 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "authentication": {
            "handlers": ["auth_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}