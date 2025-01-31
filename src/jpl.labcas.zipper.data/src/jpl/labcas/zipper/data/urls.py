# encoding: utf-8

'''🤐 Zipperlab data URL patterns.'''


from django.urls import path
from .views import generate_stream, generate_file

urlpatterns = [
    # Testing to see just how much data we can move across HTTP; first, by streaming with
    # StreamingHttpResponse
    path('stream/<int:megabytes>', generate_stream),
    # And testing with FileResponse
    path('file/<int:megabytes>', generate_file),
]
