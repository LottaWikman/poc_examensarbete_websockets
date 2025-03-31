from django.urls import path
from . import views

urlpatterns = [
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
]
