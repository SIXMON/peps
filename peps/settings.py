"""
Django settings for Peps project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('PEPS_DEBUG') == 'True'

# No need making this one secret: https://forum.sentry.io/t/dsn-private-public/6297/3
if not DEBUG:
    sentry_sdk.init(
        dsn="https://2f06863071504faf9868e6f4e99ea9db@o1143545.ingest.sentry.io/6204265",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('PEPS_SECRET')

ALLOWED_HOSTS = [x.strip() for x in os.getenv('PEPS_ALLOWED_HOSTS').split(',')]

ASANA_PERSONAL_TOKEN = os.getenv('PEPS_ASANA_PERSONAL_TOKEN')
ASANA_PROJECT = os.getenv('PEPS_ASANA_PROJECT')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'django_better_admin_arrayfield',
    'anymail',
    'webpack_loader',
    'rest_framework',
    'rest_framework_api_key',
    'peps',
    'web',
    'api',
    'data',
    'magicauth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

CSRF_COOKIE_NAME = 'csrftoken'

ROOT_URLCONF = 'peps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

OPTIONS = {
    'libraries': {
        'analytics': 'web.templatetags.analytics',
    },
}

WSGI_APPLICATION = 'peps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.getenv('PEPS_DB_USER'),
        'NAME': os.getenv('PEPS_DB_NAME'),
        'PASSWORD': os.getenv('PEPS_DB_PASSWORD'),
        'HOST': os.getenv('PEPS_DB_HOST'),
        'PORT': os.getenv('PEPS_DB_PORT'),
        'CONN_MAX_AGE': 60,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'UPLOADED_FILES_USE_URL': True,
}

MJ_APIKEY_PUBLIC = os.getenv('PEPS_MJ_APIKEY_PUBLIC'),
MJ_APIKEY_PRIVATE = os.getenv('PEPS_MJ_APIKEY_PRIVATE'),

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend/dist/')]
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': DEBUG,
        'BUNDLE_DIR_NAME': '/bundles/',
        'STATS_FILE': os.path.join(FRONTEND_DIR, 'webpack-stats.json'),
    }
}

ANALYTICS_ID = os.getenv('PEPS_ANALYTICS_ID')
ANALYTICS_DOMAIN = os.getenv('PEPS_ANALYTICS_DOMAIN')

DEFAULT_FILE_STORAGE = os.getenv('PEPS_DEFAULT_FILE_STORAGE')
STATICFILES_STORAGE = os.getenv('PEPS_STATICFILES_STORAGE')

AWS_ACCESS_KEY_ID = os.getenv('PEPS_CELLAR_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('PEPS_CELLAR_SECRET')
AWS_S3_ENDPOINT_URL = os.getenv('PEPS_CELLAR_HOST')
AWS_STORAGE_BUCKET_NAME = os.getenv('PEPS_CELLAR_BUCKET_NAME')
AWS_LOCATION = 'media'
AWS_QUERYSTRING_AUTH = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SECURE_SSL_REDIRECT = os.getenv('PEPS_FORCE_HTTPS') == 'True'

LOGIN_URL = '/login'
MAGICAUTH_FROM_EMAIL = 'agriculteur@agricultureduvivant.org'
MAGICAUTH_EMAIL_SUBJECT = 'Votre lien de connexion Rex Agri'
MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME = 'app'
MAGICAUTH_EMAIL_FIELD = 'email'
MAGICAUTH_EMAIL_HTML_TEMPLATE = 'email.html'
MAGICAUTH_EMAIL_TEXT_TEMPLATE = 'email.txt'
MAGICAUTH_LOGIN_VIEW_TEMPLATE = 'login-magicauth.html'
MAGICAUTH_EMAIL_SENT_VIEW_TEMPLATE = 'email-sent.html'
MAGICAUTH_EMAIL_UNKNOWN_MESSAGE = 'Nous n\'avons pas trouvé d\'utilisateur avec cette adresse email. Êtes-vous certain d\'avoir crée votre compte avec celle-ci ? Pour tout problème concernant votre compte utilisateur <a href="/contact">contactez-nous</a>'

MAGICAUTH_TOKEN_DURATION_SECONDS = 60 * 60 * 3

SESSION_COOKIE_AGE = 31536000

EMAIL_BACKEND = os.getenv('PEPS_EMAIL_BACKEND')

ANYMAIL = {
    "MAILJET_API_KEY": os.getenv('PEPS_MJ_APIKEY_PUBLIC'),
    "MAILJET_SECRET_KEY": os.getenv('PEPS_MJ_APIKEY_PRIVATE')
}
DEFAULT_FROM_EMAIL = "agriculteur@agricultureduvivant.org"
SERVER_EMAIL = "agriculteur@agricultureduvivant.org"

MAILJET_API_URL = "https://api.mailjet.com/v3/"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
