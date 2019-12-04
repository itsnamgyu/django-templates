"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.1.

Extended by Namgyu Ho as a custom django project template at
github.com/itsnamgyu/django-template
"""

import os
import logging

from django.core.exceptions import ImproperlyConfigured

from .env_loader import require_env, fetch_env
from .logging_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Variable to differentiate between development, staging, production etc.
# Consider changing <APP> to the name of your project. You MUST apply the
# same changes in wsgi.py
DJANGO_ENV = fetch_env("DJANGO_APP_ENV", default="DEV")

if DJANGO_ENV == "DEV":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
else:
    DEBUG = False
    ALLOWED_HOSTS = ["*"]  # change this for your real project

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
    "debug_toolbar",
    "base",
    # Carousel
    "versatileimagefield",
    "carousel",
    # Blurb
    "blurb",
    "ckeditor",
    # Admin link
    "admin_link",
    # dt-content
    "ckeditor_uploader",
    # Example
    "example",
]

SES_ENABLED = fetch_env("SES_ENABLED", "FALSE").upper() == "TRUE"
MODERN_EMAIL_ENABLED = fetch_env("MODERN_EMAIL_ENABLED", "FALSE").upper() == "TRUE"
STRIPE_ENABLED = fetch_env("STRIPE_ENABLED", "FALSE").upper() == "TRUE"
DT_STRIPE_ENABLED = fetch_env("DT_STRIPE_ENABLED", "FALSE").upper() == "TRUE"
DT_CONTENT_ENABLED = fetch_env("DT_CONTENT_ENABLED", "FALSE").upper() == "TRUE"

if DEBUG:
    # Live reload for development
    INSTALLED_APPS.insert(0, "livesync")
if MODERN_EMAIL_ENABLED:
    INSTALLED_APPS.append("modern_email")
if STRIPE_ENABLED:
    INSTALLED_APPS.append("django_stripe")
if DT_STRIPE_ENABLED:
    INSTALLED_APPS.append("dt_stripe")
if DT_CONTENT_ENABLED:
    INSTALLED_APPS.append("dt_content")

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
    static_root = fetch_env("STATIC_ROOT")
    if static_root:
        STATIC_ROOT = static_root
else:
    STATIC_ROOT = require_env("STATIC_ROOT")
    STATICFILES_STORAGE = "app.storage.LooseManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
if DEBUG:
    media_root = fetch_env("MEDIA_ROOT")
    if media_root:
        MEDIA_ROOT = media_root
    else:
        MEDIA_ROOT = os.path.join(BASE_DIR, "media")
        logging.info("Using default media root {}".format(MEDIA_ROOT))
else:
    MEDIA_ROOT = require_env("MEDIA_ROOT")

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# Blurb
CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Default",
        "toolbar_Default": [
            ["Format"],
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["Table", "Image"],
        ],
    },
    "blurb": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format"],
            ["Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
        ],
    },
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
ACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True

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
    AWS_ACCESS_KEY_ID = require_env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = require_env("AWS_SECRET_ACCESS_KEY")
    AWS_SES_REGION_NAME = fetch_env("AWS_SES_REGION_NAME", "us-west-2")
    AWS_SES_REGION_ENDPOINT = "email.{}.amazonaws.com".format(AWS_SES_REGION_NAME)

if MODERN_EMAIL_ENABLED:
    MODERN_EMAIL_STATIC_HOST = require_env("STATIC_HOST")
    MODERN_EMAIL_LOGO_IMAGE = "example/logo.png"  # TODO change this
    MODERN_EMAIL_CUSTOM_TEMPLATE = None
    MODERN_EMAIL_SUPPORT_EMAIL = "support@namgyu.io"  # TODO change this
    MODERN_EMAIL_ADDRESS_LINE_1 = "Address Line 1"  # TODO change this
    MODERN_EMAIL_ADDRESS_LINE_2 = "Address Line 2"  # TODO change this
    MODERN_EMAIL_ORGANIZATION_NAME = "Django Template Org"  # TODO change this
    MODERN_EMAIL_COPYRIGHT_START_YEAR = "2019"  # TODO change this

if DT_STRIPE_ENABLED or STRIPE_ENABLED:
    STRIPE_STATIC_HOST = require_env("STATIC_HOST")
    STRIPE_PUBLIC_KEY = require_env("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = require_env("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SIGNING_SECRET = require_env("STRIPE_WEBHOOK_SIGNING_SECRET")
    STRIPE_SUPPORT_EMAIL = "support@gyu.io"
