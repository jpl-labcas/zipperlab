# encoding: utf-8

'''🤐 Zipperlab: archiver.'''

from . import PACKAGE_NAME
from wagtail.models import Page
from django.db import models
from django.http import HttpRequest, HttpResponse
import json, uuid, logging


_logger = logging.getLogger(__name__)


class Archiver(Page):
    template = PACKAGE_NAME + '/archiver.html'

    zip_target = models.CharField(
        blank=False, null=False, default='/labcas-data/zips', max_length=1024,
        help_text='Where on the filesystem to generate ZIP archives archives'
    )

    def _initiate(self, params: dict) -> HttpResponse:
        _logger.info('🏁 Initiating for email «%s» for files %r', params['email'], params['files'])
        job_id = str(uuid.uuid4())
        _logger.info('Assigning job ID %s', job_id)
        return HttpResponse(f'{job_id} + number files = {len(params["files"])}\n', content_type='text/plain')

    def serve(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            payload = json.loads(request.body)
            if payload.get('operation') == 'initiate': return self._initiate(payload)
        return super().serve(request)
