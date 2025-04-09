from django.urls import path
from . import views

urlpatterns = [
    # Paths for the frontend-view
    path("", views.frontend_view, name="frontend-view"),
    path(
        "process-with-websocket/",
        views.process_with_websocket,
        name="start-process-with-websocket",
    ),
    path(
        "process-with-http/",
        views.process_with_http,
        name="start-process-with-http",
    ),
    # Paths for the upload-files-test-thing:
    path("upload-test", views.upload_test_view, name="upload-test-view"),
]
