# encoding: utf-8

'''🤐 Zipperlab: tasks.'''


from celery import shared_task
import logging

_logger = logging.getLogger(__name__)


@shared_task
def _send_async_email(from_addr, to, subject, body, attachment, delay):
    _logger.warning('Not implemented; taking no action')
    return
