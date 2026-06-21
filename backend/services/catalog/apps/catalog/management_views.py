"""Vendor-facing product management (scoped to the JWT vendor)."""
from rest_framework import generics

from .management_serializers import ProductWriteSerializer
from .models import Product
from .permissions import IsVendor, StatelessJWTAuthentication, acting_vendor_id
from .realtime import broadcast_product
from .serializers import ProductListSerializer


class _ManageBase:
    authentication_classes = [StatelessJWTAuthentication]
    permission_classes = [IsVendor]

    def get_queryset(self):
        return Product.objects.filter(vendor_id=acting_vendor_id(self.request)).prefetch_related("images")


class MyProductsView(_ManageBase, generics.ListCreateAPIView):
    """GET (my products) / POST (create) — /api/v1/catalog/manage/products/"""

    def get_serializer_class(self):
        return ProductWriteSerializer if self.request.method == "POST" else ProductListSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["vendor_id"] = acting_vendor_id(self.request)
        return ctx

    def perform_create(self, serializer):
        product = serializer.save()
        # 🔴 real-time: tell every connected client a product just appeared.
        broadcast_product("created", ProductListSerializer(product).data)


class MyProductDetailView(_ManageBase, generics.RetrieveUpdateDestroyAPIView):
    """GET/PATCH/DELETE — /api/v1/catalog/manage/products/<id>/"""

    lookup_field = "id"

    def get_serializer_class(self):
        return ProductWriteSerializer if self.request.method in ("PUT", "PATCH") else ProductListSerializer

    def perform_update(self, serializer):
        product = serializer.save()
        broadcast_product("updated", ProductListSerializer(product).data)

    def perform_destroy(self, instance):
        pid = str(instance.id)
        instance.delete()
        broadcast_product("deleted", {"id": pid})
