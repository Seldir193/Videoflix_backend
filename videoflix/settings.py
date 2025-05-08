from pathlib import Path
import os
from decouple import config

import datetime
import django.utils.timezone as _tz
if not hasattr(_tz, "utc"):
    _tz.utc = datetime.timezone.utc
# ---------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%%ntge@8p3=9_*bgj@$6fjzo_6^1w@&1v$uf0i)3v3n4f3iq62"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    #'videos',
     'videos.apps.VideosConfig',
     "debug_toolbar",
     'django_rq',
     'import_export',
     'users'
]

AUTH_USER_MODEL = 'users.CustomUser'


RQ_QUEUES = {
    "default": {
        #"URL": "redis://:foobared@127.0.0.1:6379/1",
        "HOST": "127.0.0.1",
        "PORT": 6379,
        "DB": 1,
        "PASSWORD": "foobared",     
        "DEFAULT_TIMEOUT": 360,
    }
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

CACHE_TTL = 60 * 15

CORS_ALLOW_CREDENTIALS = True            
CSRF_TRUSTED_ORIGINS  = [                
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CACHES = {
"default": {
"BACKEND": "django_redis.cache.RedisCache",
"LOCATION": "redis://127.0.0.1:6379/1",

"OPTIONS": {
    "PASSWORD": "foobared",
"CLIENT_CLASS": "django_redis.client.DefaultClient"
},
"KEY_PREFIX": "videoflix"
}
}

ROOT_URLCONF = "videoflix.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "videoflix",
        "USER": "vf_user",
        #"PASSWORD": os.getenv("DB_PASSWORD", "selcuk"),
         "PASSWORD": config("DB_PASSWORD"), 
        "HOST": "localhost",
        "PORT": "5432",
        "CONN_MAX_AGE": 60,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
#STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
