# routing.py

from django.urls import re_path
from .consumers import ChatConsumer

# ✅ Define WebSocket Routes
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]
