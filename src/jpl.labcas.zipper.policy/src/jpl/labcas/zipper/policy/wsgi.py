# encoding: utf-8

'''🤐 Zipperlab's Web Services Gateway Interface (WSGI).

This module must—by contract—define a name `application` that represents the WSGI
app. WSGI will load this module and look for `application`.
'''

from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jpl.labcas.zipper.policy.settings.ops')
application = get_wsgi_application()  # noqa
