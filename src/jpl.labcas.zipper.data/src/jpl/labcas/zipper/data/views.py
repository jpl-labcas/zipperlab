# encoding: utf-8

'''🤐 Zipper data: views.'''

from django.http import HttpRequest, StreamingHttpResponse, HttpResponseBadRequest, FileResponse
import logging, os, tempfile


_logger = logging.getLogger(__name__)
_chunk_size = 1024 * 1024  # megabyte


def _generate_random_bytes(megabytes: str):
    _logger.info('Generating %s megabytes of random data', megabytes)
    bytes_to_generate = int(megabytes) * _chunk_size
    while bytes_to_generate > 0:
        yield os.urandom(min(_chunk_size, bytes_to_generate))
        bytes_to_generate -= _chunk_size


def generate_stream(request: HttpRequest, megabytes: str) -> StreamingHttpResponse:
    # This simulation works if we are able to stream ZIP files, such as with
    # https://stream-zip.docs.trade.gov.uk:
    if request.method != 'GET':
        raise HttpResponseBadRequest(reason='GET only')

    # Note that Gunicorn + composition-based Nginx (and possible sysadmin-mandated Apache
    # HTTPD) eventually fails with large amounts of data
    response = StreamingHttpResponse(_generate_random_bytes(megabytes), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={megabytes}.bin'
    return response


def generate_file(request: HttpRequest, megabytes: str) -> FileResponse:
    # Suppose we first stage the ZIP files on disk; does Gunicorn + coposition-based Nginx
    # + Apache HTTPD (sysadmin required) handle it better?
    if request.method != 'GET':
        raise HttpResponseBadRequest(reason='GET only')

    tmpfile = tempfile.TemporaryFile()
    for chunk in _generate_random_bytes(megabytes):
        tmpfile.write(chunk)
    tmpfile.seek(0)
    return FileResponse(tmpfile, as_attachment=True, filename=f'{megabytes}.bin')
