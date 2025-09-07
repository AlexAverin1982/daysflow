import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ADMIN_MAIL = os.getenv('ADMIN_MAIL')
ADMIN_DEFAULT_PASSWORD = os.getenv('ADMIN_DEFAULT_PASSWORD')

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.CustomUser'

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


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# CACHE_ENABLED = False
#
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': f'{os.getenv("REDIS_HOST")}://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/1',
#     }
# }

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',  # Замените на адрес вашего фронтенд-сервера
]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

DEBUG = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# e-mail settings
DEFAULT_FROM_EMAIL = os.getenv('SERVER_MAIL_USER')
EMAIL_HOST = os.getenv('SERVER_MAIL_HOST')
EMAIL_PORT = os.getenv('SERVER_MAIL_PORT')
EMAIL_HOST_USER = os.getenv('SERVER_MAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('SERVER_MAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "groupadmin_users",
    "bootstrap_datepicker_plus",
    'users',
    'notebook',
]

LANGUAGE_CODE = "en-us"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates', os.path.join('templates', 'users'), os.path.join('templates', 'notes')],
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

TIME_ZONE = "UTC"

USE_I18N = True
USE_THOUSAND_SEPARATOR = True
USE_TZ = True

WSGI_APPLICATION = "config.wsgi.application"

SECRET_KEY = os.getenv("SECRET_KEY")
SITE_ID = 1
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"




