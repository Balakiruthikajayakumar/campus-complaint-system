"""
Django settings for campus project.
"""

import os
from pathlib import Path

# =====================================================
# BASE DIRECTORY
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# OPTIONAL: LOAD .env FILE
# =====================================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# =====================================================
# CUSTOM USER MODEL
# =====================================================
AUTH_USER_MODEL = 'accounts.user'
LOGIN_URL = 'login'

# =====================================================
# SECURITY SETTINGS
# =====================================================
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-me"
)

DEBUG = True
ALLOWED_HOSTS = []

# =====================================================
# INSTALLED APPS
# =====================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'accounts',
    'complaints',
    'outpass',
    'leave_form',
]

# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================================================
# URL CONFIG
# =====================================================
ROOT_URLCONF = 'campus.urls'

# =====================================================
# TEMPLATES
# =====================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # MAIN templates folder
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'campus.wsgi.application'

# =====================================================
# DATABASE (PostgreSQL)
# =====================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'campus_db',
        'USER': 'postgres',
        'PASSWORD': '123@srit',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# =====================================================
# PASSWORD VALIDATION
# =====================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =====================================================
# INTERNATIONAL SETTINGS
# =====================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# =====================================================
# STATIC FILES (🔥 IMPORTANT FIX AREA)
# =====================================================

# URL to access static files
STATIC_URL = '/static/'

# 🔥 This MUST point to your actual static folder
# Your structure: campus/static/
STATICFILES_DIRS = [
    BASE_DIR /  "static"
]

# For production (ignore now)
STATIC_ROOT = BASE_DIR / "staticfiles"

# =====================================================
# DEFAULT AUTO FIELD
# =====================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================================================
# EMAIL CONFIG (GMAIL)
# =====================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER