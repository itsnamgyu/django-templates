"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.1.

Extended by Namgyu Ho as a custom django project template at
github.com/itsnamgyu/django-template
"""

import logging
import os

from django.core.exceptions import ImproperlyConfigured

from .env_loader import fetch_env, require_env
from .logging_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Variable to differentiate between development, staging, production etc.
# TODO: change APP to your own prefix (must apply same prefix in `wsgi.py`)
DJANGO_ENV = fetch_env("DJANGO_APP_ENV", default="DEV")

# TODO: change this
DOMAIN = require_env("DOMAIN")

if DJANGO_ENV == "DEV":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
else:
    DEBUG = False
    ALLOWED_HOSTS = ["www." + DOMAIN, DOMAIN]

SECRET_KEY = require_env("SECRET_KEY")

# Logging (Django generated logs)
LOGGING = PRODUCTION_LOGGING

# Logging (User generated logs via `logging.log()`)
if DJANGO_ENV == "DEV":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Override logging level
LOGGING_LEVEL = fetch_env("LOGGING_LEVEL")
if LOGGING_LEVEL:
    logging.info("Setting logging level for user logs to {}".format(LOGGING_LEVEL))
    logging.basicConfig(level=LOGGING_LEVEL)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "bootstrap4",
    "base",
    # Carousel
    "versatileimagefield",
    "carousel",
    # Admin link
    "admin_link",
    # Example
    "example",
]

SES_ENABLED = fetch_env("SES_ENABLED", "FALSE").upper() == "TRUE"
SENDGRID_ENABLED = fetch_env("SENDGRID_ENABLED", "FALSE").upper() == "TRUE"
SIMPLE_SENDGRID_ENABLED = (
    fetch_env("SIMPLE_SENDGRID_ENABLED", "FALSE").upper() == "TRUE"
)
STRIPE_ENABLED = fetch_env("STRIPE_ENABLED", "FALSE").upper() == "TRUE"
DT_STRIPE_ENABLED = fetch_env("DT_STRIPE_ENABLED", "FALSE").upper() == "TRUE"
DT_CONTENT_ENABLED = fetch_env("DT_CONTENT_ENABLED", "FALSE").upper() == "TRUE"

if DEBUG:
    # Live reload for development
    INSTALLED_APPS.insert(0, "livesync")
    INSTALLED_APPS.append("debug_toolbar")
if STRIPE_ENABLED:
    INSTALLED_APPS.append("django_stripe")
if SIMPLE_SENDGRID_ENABLED:
    INSTALLED_APPS.append("simple_sendgrid")
if DT_STRIPE_ENABLED:
    INSTALLED_APPS.append("dt_stripe")
if DT_CONTENT_ENABLED:
    INSTALLED_APPS.append("dt_content")
    INSTALLED_APPS.append("django_summernote")
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SUMMERNOTE_THEME = "bs4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    # Live reload for development
    MIDDLEWARE.append("livesync.core.middleware.DjangoLiveSyncMiddleware")
    # django-debug-toolbar
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "app.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    # 'social_core.backends.google.GoogleOAuth2',  # uncomment for Google signin
    # 'social_core.backends.facebook.FacebookOAuth2',  # uncomment for Facebook signin
)

LOGGING = PRODUCTION_LOGGING

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
if DEBUG:
    STATIC_ROOT = fetch_env("STATIC_ROOT", default=None)
else:
    STATIC_ROOT = require_env("STATIC_ROOT")
    STATICFILES_STORAGE = "app.storage.LooseManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
if DEBUG:
    MEDIA_ROOT = fetch_env("MEDIA_ROOT", default=None)
    if MEDIA_ROOT is None:
        MEDIA_ROOT = os.path.join(BASE_DIR, "media")
        logging.info("Using default media root {}".format(MEDIA_ROOT))
else:
    MEDIA_ROOT = require_env("MEDIA_ROOT")

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# Summernote
SUMMERNOTE_CONFIG = {
    "iframe": False,
    "summernote": {"airMode": False, "width": "100%", "height": "640px"},
    "toolbar": [
        ["edit", ["undo", "redo"]],
        ["style", ["style"]],
        [
            "font",
            ["bold", "underline", "strikethrough", "superscript", "subscript", "clear"],
        ],
        ["para", ["ul", "ol", "paragraph"]],
        ["table", ["table"]],
        ["insert", ["link", "picture", "video", "hr"]],
        ["view", ["fullscreen", "codeview", "help"]],
    ],
}

# Django Allauth
"""
Allauth requires some manual setup on your part. Make sure to have a good
understanding of the basics and the setup process before you start. You can
read more here:
https://django-allauth.readthedocs.io/en/latest/installation.html
"""

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True

SERVER_EMAIL = "admin@" + DOMAIN
DEFAULT_FROM_EMAIL = "no-reply@" + DOMAIN

SITE_ID = 1

# Uncomment for social login
"""
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_URL_NAMESPACE = 'social'
"""

if SES_ENABLED:
    # default region for django_ses is us-east-1
    # for django-template, we set the default to us-west-2 (Oregon)
    EMAIL_BACKEND = "django_ses.SESBackend"
    logging.info("Using EMAIL_BACKEND: {}".format(EMAIL_BACKEND))
    AWS_ACCESS_KEY_ID = require_env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = require_env("AWS_SECRET_ACCESS_KEY")
    AWS_SES_REGION_NAME = fetch_env("AWS_SES_REGION_NAME", "us-west-2")
    AWS_SES_REGION_ENDPOINT = "email.{}.amazonaws.com".format(AWS_SES_REGION_NAME)

if SENDGRID_ENABLED:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    logging.info("Using EMAIL_BACKEND: {}".format(EMAIL_BACKEND))
    SENDGRID_API_KEY = require_env("SENDGRID_API_KEY")

if SIMPLE_SENDGRID_ENABLED:
    SENDGRID_TEMPLATE_ID = require_env("SENDGRID_TEMPLATE_ID")
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False

if [SES_ENABLED, SENDGRID_ENABLED].count(True) > 1:
    raise ImproperlyConfigured("Multiple email integrations enabled.")

if DT_STRIPE_ENABLED or STRIPE_ENABLED:
    STRIPE_STATIC_HOST = require_env("STATIC_HOST")
    STRIPE_PUBLIC_KEY = require_env("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = require_env("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SIGNING_SECRET = require_env("STRIPE_WEBHOOK_SIGNING_SECRET")
    # TODO: change this value
    STRIPE_SUPPORT_EMAIL = "support@gyu.io"
