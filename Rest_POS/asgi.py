import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Products.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rest_POS.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Products.routing.websocket_urlpatterns
        )
    ),
})
