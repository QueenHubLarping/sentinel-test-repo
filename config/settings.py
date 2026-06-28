"""
Minimal Django settings for the sentinel-test-repo demo app.

Storage is PostgreSQL (ADR-002). Rate limiting is intentionally NOT configured
here — it lives at the gateway (ADR-003). Email goes through Celery (ADR-001).
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "orders",
    "payments",
    "checkout",
]

# ADR-002: PostgreSQL for transactional order/payment data (not MongoDB).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE", "shop"),
        "USER": os.environ.get("PGUSER", "shop"),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "HOST": os.environ.get("PGHOST", "localhost"),
        "PORT": os.environ.get("PGPORT", "5432"),
    }
}

# ADR-001: Celery/Redis async email dispatch.
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

REST_FRAMEWORK = {
    # ADR-003: no DEFAULT_THROTTLE_CLASSES here — rate limiting is enforced at the
    # API gateway (api_gateway/nginx.conf), not in application code.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "config.urls"
