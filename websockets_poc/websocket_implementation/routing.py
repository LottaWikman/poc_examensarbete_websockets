from django.urls import re_path
from . import consumers

websocket_urlpatterns = [re_path(r'ws/socket-server/', consumers.Consumer.as_asgi())]
