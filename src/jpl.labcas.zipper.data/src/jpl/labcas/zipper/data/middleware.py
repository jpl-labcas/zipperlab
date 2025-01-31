# encoding: utf-8

'''🤐 Django middleware.

Apparently this can go away in Wagtail 6.1 which allows us to use @csrf_exempt decorators
on the "serve" method, but we're not at that version yet.

'''

from django.middleware.csrf import CsrfViewMiddleware
from wagtail.views import serve
from ._archiver import Archiver


class ArchiverExemptingCSRFViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        '''Process a view for a Wagtail page checking for Archiver and exempt it from CSRF
        checks.

        See wagtail/wagtail#3066.
        '''

        # This only works for the first Archiver object though. UGH!
        # 
        # Fine, turning off all CSRF protection.
        if callback == serve:
            page = Archiver.objects.first()
            path = callback_args[0]
            if page and path.startswith(page.get_url_parts()[-1][1:]):
                return None

        return super().process_view(request, callback, callback_args, callback_kwargs)
