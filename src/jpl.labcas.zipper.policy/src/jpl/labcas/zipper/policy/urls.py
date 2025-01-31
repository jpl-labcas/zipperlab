# encoding: utf-8

'''🤐 Zipperlab URL patterns.'''


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.contrib.auth import views as auth_views
from jpl.labcas.zipper.data.urls import urlpatterns as data_urlpatterns

urlpatterns = data_urlpatterns + [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'', include(wagtail_urls)),
]

# Note: we wouldn't normally want to serve static files or media out of the `urlpatterns` listed
# here. This means that the Django app is doing unnecessary work. However, in order to Dockerize
# this app, it does make sense to at laeast provide a fallback for Django (+ wsgi + gunicorn) to do
# the work in order to be completely containerized.
#
# So we do include the static files and media URL patterns to support this. However, in an optimal
# deployment, the ALB (or Nginx or Apache HTTPD or whatever) would intercept /static and /media URLs
# and serve them directly out of the host filesystem.
#
# 🤔 Think this through. Disable for now to confirm that running from a container actually works
#
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
