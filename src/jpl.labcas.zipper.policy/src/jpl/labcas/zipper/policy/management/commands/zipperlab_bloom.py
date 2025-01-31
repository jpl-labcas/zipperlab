# encoding: utf-8

'''🤐 Zipperlab: site bloomer.'''


from django.conf import settings
from django.core.management.base import BaseCommand
from jpl.labcas.zipper.data.models import Archiver
from wagtail.models import Site
import argparse


class Command(BaseCommand):
    help = 'Blooms Zipperlab with initial content'
    _hostname = 'labcas-dev.jpl.nasa.gov'
    _port = 80

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--hostname', help='Hostname of the site (default: %(default)s)', default=self._hostname)
        parser.add_argument('--port', help='Port of the site (default %(default)s)', default=self._port, type=int)

    def _set_site(self, hostname: str, port: int):
        '''Set up the Wagtail `Site` object for Zipperlab and return it.'''

        self.stdout.write('Setting up Wagtail "Site" object')
        site = Site.objects.filter(is_default_site=True).first()
        site.site_name, site.hostname, site.port = 'Zipperlab', hostname, port
        site.save()
        # old_root = site.root_page.specific
        # if old_root.title == 'Zipperlab':
        #     # No action needed
        #     return site, old_root

        site.save()
        return site

    def _add_archiver(self, site):
        site.root_page.get_children().all().delete()
        site.root_page.refresh_from_db()
        archiver = Archiver(title='Early Detection Research Network', slug='edrn')
        site.root_page.add_child(instance=archiver)
        archiver.save()

    def handle(self, *args, **options):
        self.stdout.write('Blooming "Zipperlab" site')

        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False

            site = self._set_site(options['hostname'], options['port'])  # noqa
            self._add_archiver(site)

        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
