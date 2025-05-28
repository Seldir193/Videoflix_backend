from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
import datetime
import django.utils.timezone as _tz
if not hasattr(_tz, "utc"):
    _tz.utc = datetime.timezone.utc

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv('SECRET_KEY')



DEBUG = os.getenv("DEBUG", "True").lower() == "true"

#DOMAIN = "localhost"  
DOMAIN = "localhost:4200"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", default="http://localhost:4200").split(",")


INSTALLED_APPS = [
    # 1) 3rd-party translation engine zuerst
    "modeltranslation",

    # 2) sonstige Third-Party-Middleware (cors, etc.)
    "corsheaders",

    # 3) Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    
    # 4) deine eigenen / übrigen Apps
    "videos.apps.VideosConfig",   # <– benutzt jetzt modeltranslation korrekt
    "users",

  

    # 5) REST & Tools
    "rest_framework",
    "djoser",
    "rest_framework_simplejwt",
    "import_export",
    "django_rq",
    "debug_toolbar",
   # 'rest_framework.authtoken',
]


SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


DJOSER = {
    "LOGIN_FIELD": "email",
    "TOKEN_MODEL": None,
    "USER_CREATE_PASSWORD_RETYPE": True, 
    'USER_CREATE_PASSWORD_CONFIRM': True,
    
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_PASSWORD_RESET_EMAIL": True, 
    #  "ACTIVATION_URL": "activate/{uid}/{token}",
   "ACTIVATION_URL": "auth/activate/{uid}/{token}",
   
    #"PASSWORD_RESET_CONFIRM_URL": "auth/password_reset_confirm/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL":  "auth/reset-password/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "user": "users.serializers.UserSerializer",
    },
    "PASSWORD_RESET_EMAIL": "users/email/reset_password.html",

}



AUTH_USER_MODEL = 'users.CustomUser'

# Simple-JWT Feintuning
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
    
   
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





CORS_EXPOSE_HEADERS = ["Content-Range", "Accept-Ranges"]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CACHE_TTL = 60 * 15

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
   
    

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    
     'django.middleware.locale.LocaleMiddleware',
    
    
    
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_LOCATION", default="redis://redis:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "videoflix"
    }
}

ROOT_URLCONF = "videoflix.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ BASE_DIR / 'templates',  ],
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

WSGI_APPLICATION = "videoflix.wsgi.application"


#DATABASES = {
    #"default": {
       # "ENGINE": "django.db.backends.postgresql",
       # "NAME": os.environ.get("DB_NAME", default="videoflix_db"),
      #  "USER": os.environ.get("DB_USER", default="videoflix_user"),
      #  "PASSWORD": os.environ.get("DB_PASSWORD", default="supersecretpassword"),
        #"HOST": os.environ.get("DB_HOST", default="db"),
       # "PORT": os.environ.get("DB_PORT", default=5432)
   # }
#}



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

LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ('en', 'English'),
    ('de', 'Deutsch'),
)


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


 #EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
 #EMAIL_HOST = os.getenv("EMAIL_HOST", default="smtp.example.com")
 #EMAIL_PORT = os.getenv("EMAIL_PORT", default=587)
 #EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
 #EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
 #EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
 #EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
 #DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")


if DEBUG:
    # Entwicklungsmodus: Mailinhalt erscheint in der Konsole
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

else:
    # Production: echte SMTP-Daten aus ENV-Variablen
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")          # z. B. smtp.yourhost.com
    EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
    # z. B. api@videoflix.com
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # SMTP-Passwort
    EMAIL_USE_TLS = True                             # meist 587 + TLS

# Absenderadresse für alle Systemmails
DEFAULT_FROM_EMAIL = "noreply@videoflix.local"





CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "X-CSRFToken"

CORS_ALLOW_CREDENTIALS = True



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