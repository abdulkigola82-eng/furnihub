import os
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY haijawekwa kwenye mazingira ya hosting.")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

if not ALLOWED_HOSTS:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS haijawekwa kwenye mazingira ya hosting.")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *[m for m in MIDDLEWARE if m != "django.middleware.security.SecurityMiddleware"],
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Production email configuration: values come from hosting environment.
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "HOST": os.environ.get("EMAIL_HOST", ""),
        "PORT": int(os.environ.get("EMAIL_PORT", "587")),
        "USERNAME": os.environ.get("EMAIL_HOST_USER", ""),
        "PASSWORD": os.environ.get("EMAIL_HOST_PASSWORD", ""),
        "USE_TLS": os.environ.get("EMAIL_USE_TLS", "True").lower() == "true",
    },
}
