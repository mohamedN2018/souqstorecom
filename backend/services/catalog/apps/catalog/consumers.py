"""
WebSocket consumer for the live product feed.

Clients (storefront + vendor dashboard) connect to /ws/products/ and join the
"products" group. When a vendor creates/updates a product, the API broadcasts
to this group and every connected client updates instantly — no refresh.
"""
import json

from channels.generic.websocket import AsyncWebsocketConsumer

PRODUCTS_GROUP = "products"


class ProductFeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(PRODUCTS_GROUP, self.channel_name)
        await self.accept()
        await self.send(json.dumps({"type": "connected"}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(PRODUCTS_GROUP, self.channel_name)

    # Handler for messages sent to the group with type "product.event".
    async def product_event(self, event):
        await self.send(text_data=json.dumps(event["payload"]))
