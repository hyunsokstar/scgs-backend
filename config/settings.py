"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

import os
import environ
import dj_database_url

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-ba(7an6)02(9^sw$kge33^#1$0vc*y$6z45cts(8hyb@1ecl&1"
SECRET_KEY = env("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = True

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "houses.apps.HousesConfig",
# ]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "direct_messages.apps.DirectMessagesConfig",
    "estimate.apps.EstimateConfig",
    "tutorials.apps.TutorialsConfig",
    "project_progress.apps.ProjectProgressConfig",
    "tech_note.apps.TechNoteConfig",
    "api_docu.apps.ApiDocuConfig",
    "shortcut.apps.ShortcutConfig",
    "shortcut2.apps.Shortcut2Config",
]

SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    # "corsheaders"
]

INSTALLED_APPS = CUSTOM_APPS + THIRD_PARTY_APPS + SYSTEM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'django_brotli.middleware.BrotliMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    """
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
        )
    }
    """
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env('DATABASE_NAME'),
            "USER": env('DATABASE_USER'),
            "PASSWORD": env('DATABASE_PASSWORD'),
            "HOST": env('DATABASE_HOST'),
            "PORT": 3306,
            "OPTIONS": {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# DEBUG = True or False
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": env('DATABASE_NAME'),
#         "USER": env('DATABASE_USER'),
#         "PASSWORD": env('DATABASE_PASSWORD'),
#         "HOST": env('DATABASE_HOST'),
#         "PORT": 3306,
#         "OPTIONS": {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"
TIME_ZONE = 'Asia/Seoul'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'www_dir'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"
MEDIA_ROOT = "uploads"
MEDIA_URL = "user-uploads/"

PAGE_SIZE = 3


# 장고 인증 클래스 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "config.authentication.TrustMeBroAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "config.authentication.JWTAuthentication",
    ]
}

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://13.125.214.210"]
CORS_ALLOW_CREDENTIALS = True

CF_ID = env("CF_ID")
CF_TOKEN = env("CF_TOKEN")

# 네이버 메일 보내기
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    'http://localhost',
    'http://localhost:3000',
    'http://13.125.214.210',
    'http://12.125.214.210:3000',
    'http://12.125.214.210:8000'
]
