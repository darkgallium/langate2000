"""
Django settings for langate project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from enum import Enum
import os

from modules import network

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# If you get a warning, be sure to have the variable SECRET_KEY populated into the file secret_settings.py
try:
    from langate.settings_local import *
except ModuleNotFoundError:
    SECRET_KEY = 'secret'
    print("[WARN] Secret settings not found, the website isn't secure anymore.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SERVER_IP = '172.16.1.197'

ALLOWED_HOSTS = ['localhost', SERVER_IP]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
    'bootstrap4',
    'rest_framework',
    'helpdesk'
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

ROOT_URLCONF = 'langate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'langate.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Authentication

LOGIN_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = ('langate.insalan_auth.insalan_backend.InsalanBackend',)

# Network management

#netmgt = Ipset()

# Widgets content

WIDGETS = {
    "PIZZA": {
        "visible": True,
        "link": "https://www.insalan.fr/pizza",
        "schedule": ["18h-20h, livraison à 21h30.", "20h-22h, livraison à 22h30."],
    },

    "ANNOUNCE": {
        "visible": False,
        "content": 'Nous rencontrons actuellement des problèmes de stabilité de notre accès internet.\n' +
                   'Nos équipes sont à pied d\'oeuvre pour résoudre ce problème dans les plus brefs délais.\n' +
                   'Nous vous remercions de votre patience.'
    },

    "STATUS": {
        "visible": True,
        "network_up": True,
        "internet_up": True,
        "csgo_up": True
    }
}


# Tournament list

class Tournament(Enum):
    cs = "Counter Strike Global Offensive"
    ftn = "Fortnite"
    hs = "Heartstone"
    lol = "League Of Legends"


# Network management interface

NETWORK = network.Ipset()


# Logging settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,


    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] [{module}] {message}',
            'style': '{',
        },
    },

    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },

        'langate_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/langate.log'),
        },
    },

    'loggers': {
        'django': {
            'handlers': ['django_file'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'langate.events': {
            'handlers': ['langate_file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
