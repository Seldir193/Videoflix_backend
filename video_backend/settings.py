
import django.utils.timezone as _tz
import datetime
from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SITE_ID = 1

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", default="http://localhost:4200").split(",")

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://videoflix.selcuk-kocyigit.de",
]

AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    "accounts",
    'modeltranslation',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_rq',
    'rest_framework',
    'import_export',
    'debug_toolbar',
    'djoser',
    'corsheaders',
    'django.template',
    'whitenoise',
    "django.contrib.sites",
    "videos.apps.VideosConfig",
    "users",
    "rest_framework_simplejwt",
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'debug_toolbar.middleware.DebugToolbarMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
]

ROOT_URLCONF = "video_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = "video_backend.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'videoflix_db'),
        'USER': os.environ.get('DB_USER', 'vf_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'selcuk'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION", default="redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "video_backend"
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': os.environ.get("REDIS_HOST", default="redis"),
        'PORT': os.environ.get("REDIS_PORT", default=6379),
        'DB': os.environ.get("REDIS_DB", default=0),
        'DEFAULT_TIMEOUT': 900,
        'REDIS_CLIENT_KWARGS': {},
    },
}


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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


FRONTEND_PROTOCOL = os.getenv("FRONTEND_PROTOCOL", "http")
FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN",   "localhost:4200")

ACTIVATION_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}/auth/activate/{{uid}}/{{token}}"
PASSWORD_RESET_CONFIRM_URL = f"{FRONTEND_PROTOCOL}://{FRONTEND_DOMAIN}/auth/reset-password/{{uid}}/{{token}}"


DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_PASSWORD_RESET_EMAIL": True,
    "EMAIL_FRONTEND_PROTOCOL": FRONTEND_PROTOCOL,
    "EMAIL_FRONTEND_DOMAIN":   FRONTEND_DOMAIN,
    "ACTIVATION_URL": "auth/activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "auth/reset-password/{uid}/{token}",

    "EMAIL": {
        "activation": "accounts.email.CustomActivationEmail",
        "password_reset": "accounts.email.CustomPasswordResetEmail",
    },

    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "user":        "users.serializers.UserSerializer",
    },
}


EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = os.getenv("EMAIL_HOST", "w01f330f.kasserver.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
    EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
    DEFAULT_FROM_EMAIL = os.getenv(
        "DEFAULT_FROM_EMAIL", "Videoflix <noreply@videoflix.selcuk-kocyigit.de>"
    )

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "X-CSRFToken"
CORS_ALLOW_CREDENTIALS = True

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ('de', 'German'),
    ('en', 'English'),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

WHITENOISE_ADD_HEADERS = True
STATIC_URL = "/static/"
#STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [BASE_DIR / "static"] 
STATIC_ROOT = BASE_DIR / "staticfiles" 

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 86400

WHITENOISE_USE_FINDERS = True

WHITENOISE_KEEP_ONLY_HASHED_FILES = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CACHE_TTL = 60 * 15
