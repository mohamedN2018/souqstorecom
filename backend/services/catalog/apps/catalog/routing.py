from django.urls import path

from .consumers import ProductFeedConsumer

websocket_urlpatterns = [
    path("ws/products/", ProductFeedConsumer.as_asgi()),
]
