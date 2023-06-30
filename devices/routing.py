# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/live_data/<str:room_name>/", consumers.SendLiveData.as_asgi()),
]
