# encoding: utf-8

'''🤐 Zipperlab: development settings.'''

from .base import *  # noqa: F401, F403


# Debug Mode
# ----------
#
# In development we want debug mode of course!
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = True


# Templates
# ---------
#
# FEC practice: add a 'debug' flag to every template
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = globals().get('TEMPLATES', [])
for t in TEMPLATES:  # noqa: F405
    t.setdefault('OPTIONS', {})
    t['OPTIONS']['debug'] = True


# Email Backend
# -------------
#
# How to send email while in debug mode: don't! The FEC practice: write emails to stdout.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#email-backend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Site Identification
# -------------------
#
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-site-name

WAGTAIL_SITE_NAME = '🔧 Dev Zipperlab'


# Debugging & Development Tools
# -----------------------------
#
# 🔗 https://docs.wagtail.io/en/stable/contributing/styleguide.html
# 🔗 https://pypi.org/project/django-extensions/
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips

INSTALLED_APPS += [  # noqa
    'wagtail.contrib.styleguide',
    'django_extensions',
]
