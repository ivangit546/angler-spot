from django.urls import re_path
from angler.consumers import ChatroomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<gc_id>\d+)/$', ChatroomConsumer.as_asgi()),
]