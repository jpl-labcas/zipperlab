# encoding: utf-8

'''🤐 Zipperlab: tasks.'''


from celery import shared_task
from django.core.mail.message import EmailMessage
import logging, zipfile, os.path, os, time, base64, traceback

_logger = logging.getLogger(__name__)


_user_failure_template = '''We're sorry to report that we ran into a problem when creating your ZIP archive.

The exact error message was: {error_message}.

This has been logged and an administrator will be taking a look to see what went wrong.

In the meantime, you can revisit {url} and try again. If you have any questions, please contact is.

— ic-data@jpl.nasa.gov'''


_admin_failure_template = '''ZIP archive failed to create for user with email {email}.

Error was: {error_message}. The stack trace is as follows:

{stack_trace}
'''

_user_success_template = '''Your ZIP archive requested through LabCAS is ready for downloading.

You can download the ZIP file at this URL: {zip_url}

Please note that ZIP files are automatically cleaned up every 7 days, so please try to download your file promptly.

Feel free to return to {url} to explore and download more scientific data.

Thanks,
— ic-data@jpl.nasa.gov
'''


@shared_task
def _send_email_asynchronously(from_addr, to, subject, body, attachment, delay):
    _logger.info('✉️ Sending email async to "%s" from "%s" with delay %d', to, from_addr, delay)
    time.sleep(delay)
    if attachment:
        a = [(attachment['name'], base64.b64decode(attachment['data']), attachment['content_type'])]
        _logger.info('Making EmailMessage, subject = %s', subject)
        _logger.info('from_email = %s', from_addr)
        _logger.info('to = %r', to)
        _logger.info('attachments = %r', a)
        _logger.info('body = %s', body)
        message = EmailMessage(subject=subject, from_email=from_addr, to=to, attachments=a, body=body)
    else:
        message = EmailMessage(subject=subject, from_email=from_addr, to=to, body=body)
    message.send()


def send_email(from_addr, to, subject, body, attachment=None, delay=1):
    _logger.info('✉️ send_email from %s to %s subject %s', from_addr, to, subject)
    if attachment:
        for field in ('name', 'data', 'content_type'): assert field in attachment
        attachment['data'] = base64.b64encode(attachment['data']).decode('utf-8')
    _send_email_asynchronously.delay(from_addr, to, subject, body, attachment, delay)


@shared_task
def do_send_async_email(from_addr, to, subject, body, attachment, delay):
    _logger.warning('Not implemented; not sending email')


@shared_task
def do_create_zip(uuid, output_dir, to_email, files, from_addr, url):
    try:
        target, count = os.path.join(output_dir, uuid) + '.zip', 0
        _logger.info('🤐 Creating zip archive in %s', target)
        os.makedirs(output_dir, exist_ok=True)

        # Tested ZIP_BZIP2 and ZIP_LZW and they took longer for sure but also produced larger
        # ZIP archives with my test data; so sticing with ZIP_DEFLATED which has wide-spread
        # compatibility.
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                archive_name = file[1:]
                if os.path.isfile(file):
                    zipf.write(file, archive_name)
                    count += 1
        _logger.info('🤐 Done with %s, wrote %d files', target, count)
        if not url.endswith('/'): url += '/'
        body = _user_success_template.format(zip_url=f'{url}zips/{uuid}.zip', url=url)
        send_email(from_addr, [to_email], 'Your LabCAS ZIP archive is ready to download', body)

    except Exception as ex:
        _logger.exception('😖 Exception %s while handling zipping for %s (job %s)', ex, to_email, uuid)
        body = _user_failure_template.format(error_message=str(ex), url=url)
        send_email(from_addr, [to_email], 'We ran into a problem creating your ZIP archive', body)
        body = _admin_failure_template.format(
            email=to_email, error_message=str(ex), stack_trace=traceback.format_exc()
        )
        send_email(from_addr, [from_addr], "An error occurred generating a user's ZIP file", body)
