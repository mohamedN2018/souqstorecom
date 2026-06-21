"""Helper to broadcast product events to all connected WebSocket clients."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .consumers import PRODUCTS_GROUP


def broadcast_product(action: str, product_data: dict) -> None:
    """action: 'created' | 'updated' | 'deleted'."""
    layer = get_channel_layer()
    if layer is None:
        return
    async_to_sync(layer.group_send)(
        PRODUCTS_GROUP,
        {
            "type": "product_event",
            "payload": {"event": f"product.{action}", "product": product_data},
        },
    )
