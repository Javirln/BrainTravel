"""
Django settings for BrainTravel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wt25dtpbzg9ks8l891^2f+hui6uqux&2s*)9@jxj20i9%=q98s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

FILE_CHARSET = 'ISO-8859-1'


# Application definition

INSTALLED_APPS = (
    # 'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'principal',
    'paypal.standard.ipn',

)

#PAYPAL_IDENTITY_TOKEN = "GNkgEreFTTFHaMggPfcTun98GZBOIEZzvIRJy3P00hEnMWuIQ9uQPspAVX0"

MIDDLEWARE_CLASSES = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# Dir for i18n
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

ROOT_URLCONF = 'BrainTravel.urls'

WSGI_APPLICATION = 'BrainTravel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'braintravel',
        'USER': 'braintravel',
        'PASSWORD': 'bR@1nTr@veL',
        'HOST': 'mysql.cvu77qxolqzd.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'ATOMIC_REQUESTS': 'True'
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "/principal/templates"),
    os.path.join(BASE_DIR, "/principal/emailTemplates"),
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/signin/'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'notificaciones.braintravel@gmail.com'
EMAIL_HOST_PASSWORD = 'braintravelredmine'

# PAYPAL CONFIGURATION
PAYPAL_RECEIVER_EMAIL = 'braintravel.payments-facilitator@gmail.com'
PAYPAL_TEST = True