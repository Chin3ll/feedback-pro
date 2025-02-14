
from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-08x%jr)=yx_0ac@9(7n9elld+l_oikck2hvt9db=+pl#_ody95'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

from decouple import config
from django.contrib.sites.shortcuts import get_current_site


# COHERE_API_KEY = config('COHERE_API_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorting_feedback',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'feedback_sorting.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],  # Ensure templates directory is set
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'feedback_sorting.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
        "default": {
            "ENGINE": "mysql.connector.django",
            "NAME": "feedbackgenerator",
            "USER": "root",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "3306",
            "OPTIONS": {
                "autocommit": True,
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

CRISPY_TEMPLATE_PACK = 'bootstrap5'  # Change to 'bootstrap4' if using Bootstrap 4


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'#Location of static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'  # Change this to your actual login page URL


# Looking to send emails in production? Check out our Email API/SMTP product!
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'd21b3efded16ab'
EMAIL_HOST_PASSWORD = 'bd62864bd40fb8'
EMAIL_PORT = '2525'
DEFAULT_FROM_EMAIL = EMAIL_HOST
EMAIL_USE_TLS = True



PASSWORD_RESET_TIMEOUT = 3600  # 1-hour expiry

PASSWORD_RESET_CONFIRM_URL = "password-reset-confirm"