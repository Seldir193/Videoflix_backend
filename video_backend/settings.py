import os
import datetime
from datetime import timedelta
from pathlib import Path
from re import DEBUG

import django.utils.timezone as _tz
from dotenv import load_dotenv

# === BASE ===
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# === BASIC SETTINGS ===
SITE_ID = 1
#DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "http://localhost:4200"
).split(",")

# === CORS ===
CORS_ALLOWED_ORIGINS = [
    "https://videoflix.selcuk-kocyigit.de",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
CORS_ALLOW_CREDENTIALS = True

# === AUTH ===
AUTH_USER_MODEL = "users.CustomUser"

# === INSTALLED APPS ===
INSTALLED_APPS = [
    "accounts",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "videos.apps.VideosConfig",
    "users",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "corsheaders",
    "django.template",
    "import_export",
    "debug_toolbar",
    "django_rq",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",   
    "whitenoise.middleware.WhiteNoiseMiddleware",      
    "corsheaders.middleware.CorsMiddleware",           
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


# === URL/WSGI ===

ROOT_URLCONF = "video_backend.urls"
WSGI_APPLICATION = "video_backend.wsgi.application"

# === TEMPLATES ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# === DATABASE ===  ORIGINAL

DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "videoflix_db"),
        "USER": os.getenv("DB_USER", "real_db_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "very_secret_pw"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/1",          # Default für Docker-Compose
)

# === CACHE / REDIS ===
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "video_backend",
    }
}

RQ_QUEUES = {
    "default": {
        "URL": REDIS_URL,             # <-- nur eine Zeile!
        "DEFAULT_TIMEOUT": 900,
    }
}


# === PASSWORD VALIDATORS ===
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# === REST FRAMEWORK ===
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

# === FRONTEND CONFIG ===
FRONTEND_PROTOCOL = os.getenv("FRONTEND_PROTOCOL", "http")
FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "localhost:4200")

ACTIVATION_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}/auth/activate/{{uid}}/{{token}}"
PASSWORD_RESET_CONFIRM_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}/auth/reset-password/{{uid}}/{{token}}"

# === DJOSER CONFIG ===
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_PASSWORD_RESET_EMAIL": True,
    "EMAIL_FRONTEND_PROTOCOL": FRONTEND_PROTOCOL,
    "EMAIL_FRONTEND_DOMAIN": FRONTEND_DOMAIN,
    "ACTIVATION_URL": "auth/activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "auth/reset-password/{uid}/{token}",
    "EMAIL": {
        "activation": "accounts.email.CustomActivationEmail",
        "password_reset": "accounts.email.CustomPasswordResetEmail",
    },
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "user": "users.serializers.UserSerializer",
    },
}

# === EMAIL ===
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
    DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "Videoflix <noreply@example.com>",
)

# === JWT ===
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# === SECURITY / COOKIES ===
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "X-CSRFToken"

# === INTERNATIONALIZATION ===
LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("de", "German"),
    ("en", "English"),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# === STATIC & MEDIA ===
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

WHITENOISE_MAX_AGE = 86400
WHITENOISE_USE_FINDERS = True
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_AUTOREFRESH = DEBUG

# === MISC ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INTERNAL_IPS = ["127.0.0.1"]
CACHE_TTL = 60 * 15

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedStaticFilesStorage"  
)


# production only
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#WHITENOISE_AUTOREFRESH = False
