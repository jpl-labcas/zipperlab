# encoding: utf-8

'''🤐 Zipperlab: archiver.'''

from . import PACKAGE_NAME
from .tasks import do_create_zip
from wagtail.models import Page
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.conf import settings
from wagtail.admin.panels import FieldPanel
import json, uuid, logging, os.path


_logger = logging.getLogger(__name__)


class Archiver(Page):
    template = PACKAGE_NAME + '/archiver.html'

    zip_target = models.CharField(
        blank=False, null=False, default='/labcas-data/zips', max_length=1024,
        help_text='Where on the filesystem to generate ZIP archives archives'
    )
    max_zip_size = models.FloatField(
        blank=False, default=1.8, help_text='Maximum size of a ZIP file before balking, in gigabytes'
    )
    labcas_url = models.URLField(
        blank=False, null=False, default='https://edrn-labcas.jpl.nasa.gov/',
        help_text='URL of LabCAS (inserted for convenience into notification emails)'
    )
    from_email = models.EmailField(
        blank=False, null=False, default='ic-data@jpl.nasa.gov',
        help_text='"From" email address for notification emails'
    )
    content_panels = Page.content_panels + [
        FieldPanel('zip_target'),
        FieldPanel('max_zip_size'),
        FieldPanel('labcas_url'),
        FieldPanel('from_email')
    ]

    def _transform_path(self, path: str) -> str:
        return path.replace('/labcas-data', '/Users/kelly') if settings.DEBUG else path

    def _estimate_zip_size(self, files: list[str], compression_ratio=0.5) -> int:
        total_size = 0
        for file_path in files:
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                _logger.info('📏 File %s has size %d', file_path, file_size)
                compressed_size = int(file_size * compression_ratio)
                total_size += compressed_size
            else:
                _logger.info('📏 File %s not found or is not a file', file_path)
        return total_size

    def _initiate(self, params: dict) -> HttpResponse:
        _logger.info('🏁 Initiating for email «%s» for %d files', params['email'], len(params['files']))
        email, files = params['email'], [self._transform_path(f) for f in params['files']]

        # Check size
        total_size = self._estimate_zip_size(files)
        if total_size > self.max_zip_size * (1024 ** 3):
            _logger.info('🚛 ZIP estimate %d exceeds max of %f', total_size, self.max_zip_size)
            return HttpResponseBadRequest(f'Estimated ZIP size of {total_size} exceeds max {self.max_zip_size} GB')

        job_id = str(uuid.uuid4())
        _logger.info('Assigning job ID %s', job_id)
        do_create_zip.delay(job_id, self.zip_target, email, files, self.from_email, self.labcas_url)
        return HttpResponse(f'{job_id}\n', content_type='text/plain')

    def serve(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            payload = json.loads(request.body)
            if payload.get('operation') == 'initiate': return self._initiate(payload)
        return super().serve(request)
