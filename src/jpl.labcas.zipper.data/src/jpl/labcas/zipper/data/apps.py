# encoding: utf-8

'''🤐 Django app config.'''

from . import PACKAGE_NAME
from django.apps import AppConfig


class ZipperDataConfig(AppConfig):
    '''The Zipper data app.'''
    name = PACKAGE_NAME
    label = 'jpllabcaszipperdata'
    verbose_name = 'Zipper data'
