"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-en3ad2_-src88ki*1mg*jd&gl!q%jo&lm1j@yrmp2gfvj$suvt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'dashbord',
    'products',
    'captcha',
    'social_django',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'dbadvante',
        'USER' : 'root',
        'PASSWORD' : 'kumahaweh123',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'

LOGIN_URL = 'sign'

# Pengaturan sesi
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 2592000  # Sekitar 30 hari dalam detik

# Pengaturan otentikasi
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication
]

RECAPTCHA_PUBLIC_KEY = '6Lcir6wnAAAAALUICRtke6E3Ypb0yvnRWPElDsje'
RECAPTCHA_PRIVATE_KEY = '6Lcir6wnAAAAAJHRLJFd9jQbEUo7bF3cz-odoq37'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']   

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '13751664027-jc0m9sdpgbpngb81ehgs17692jtstk50.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'accounts.pipeline.check_email_exists',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# settings.py

import os

# ...

# Membuat direktori untuk log kesalahan jika belum ada
if not os.path.exists('logs'):
    os.makedirs('logs')

# Konfigurasi logging
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = 'DEBUG'  # Sesuaikan level log sesuai kebutuhan Anda (DEBUG, INFO, ERROR, dll.)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
        },
    },
    'root': {
        'handlers': ['file'],
        'level': LOGGING_LEVEL,
    },
}


MEDIA_URL = '/home/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BING_MAPS_API_KEY = 'ArNisPgwcsQaOmrhXYU4WDFykrY0btbKoTssZYNJNW0cI1IaXuKhiuOywAP8jPf_'


DATA_UPLOAD_MAX_MAXMEMORY_SIZE = 5242880

from django.utils import timezone
# settings.py

TIME_ZONE = 'Asia/Jakarta'  # Ganti dengan zona waktu yang sesuai dengan kebutuhan Anda
