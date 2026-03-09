from channels.routing import URLRouter

from messaging.routing import websocket_urlpatterns

websocket_routing = URLRouter(websocket_urlpatterns)
