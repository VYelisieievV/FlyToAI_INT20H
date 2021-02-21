"""
Django settings for bakery project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from corsheaders.defaults import default_headers

import pandas as pd
import os
import sys



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#DATA = pd.read_csv("/app/server_django/bakery/cake/2020+2019_cluster.csv")
CURRENT_DIR = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p9e16^dzs&lme%r0jcc@klbbi^2vodb58igdylw@wdjd#d=c2q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CACHE = False

ALLOWED_HOSTS = ['ec2-63-33-82-178.eu-west-1.compute.amazonaws.com',
                 'ec2-54-73-215-109.eu-west-1.compute.amazonaws.com',
                '172.31.15.229',
                 'localhost',
                 'ip-10-0-2-13.eu-west-1.compute.internal']
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = [
    'cake',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost',
    'http://localhost:3000',
    'http://cash-assist.s3-website-eu-west-1.amazonaws.com',
    'https://d28x4bif25eid1.cloudfront.net',
]

CORS_ALLOW_METHODS = [
    'POST',
    'GET',
]

CORS_ALLOW_HEADERS = list(default_headers) + ['cluster']

ROOT_URLCONF = 'bakery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bakery/templates')],
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

TEMPLATE_DIRS = (
    PROJECT_PATH + '/templates/',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

WSGI_APPLICATION = 'bakery.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#DATABASES = {
# 
#    'default': {
#     
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': 'root',
#        'PASSWORD': 'bakery.2020',
#        'NAME': 'cache_requests',
#        'HOST': 'db',
#        'PORT': '3306'
#        
#        },
#        
#    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'cake', 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'cake', 'media/')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/plot'