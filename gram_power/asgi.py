import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from devices import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_power .settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))),
}
)
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#                 path("ws/live_data/<str:room_name>/", consumers.SendLiveData.as_asgi()),
#             ])
#         )
#     ),
# })
