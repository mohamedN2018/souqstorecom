from django.utils.text import slugify
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .management_serializers import (
    ThemeUpdateSerializer,
    VendorRegisterSerializer,
    VendorUpdateSerializer,
)
from .models import StoreTheme, Vendor
from .permissions import IsVendor, StatelessJWTAuthentication
from .serializers import VendorDetailSerializer


class _VendorBase(GenericAPIView):
    authentication_classes = [StatelessJWTAuthentication]
    permission_classes = [IsVendor]

    def my_store(self):
        return Vendor.objects.filter(owner_id=self.request.user.id).select_related("theme").first()


class VendorRegisterView(_VendorBase):
    """POST /api/v1/vendors/register/ — the logged-in vendor opens their store."""

    serializer_class = VendorRegisterSerializer

    def post(self, request):
        if self.my_store():
            return Response({"detail": "Store already exists."}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        base_slug = slugify(name, allow_unicode=True) or "store"
        slug, i = base_slug, 1
        while Vendor.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{i}"
            i += 1

        # New stores start PENDING — the admin reviews & approves after contact.
        vendor = Vendor.objects.create(
            owner_id=request.user.id, slug=slug, status="pending",
            **serializer.validated_data,
        )
        StoreTheme.objects.create(vendor=vendor)  # sensible defaults
        return Response(VendorDetailSerializer(vendor).data, status=status.HTTP_201_CREATED)


class MyStoreView(_VendorBase):
    """GET/PATCH /api/v1/vendors/me/ — read or update my store profile."""

    serializer_class = VendorUpdateSerializer

    def get(self, request):
        store = self.my_store()
        if not store:
            return Response({"detail": "No store yet."}, status=status.HTTP_404_NOT_FOUND)
        return Response(VendorDetailSerializer(store).data)

    def patch(self, request):
        store = self.my_store()
        if not store:
            return Response({"detail": "No store yet."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(VendorDetailSerializer(store).data)


class MyThemeView(_VendorBase):
    """PATCH /api/v1/vendors/me/theme/ — the store owner controls its colors."""

    serializer_class = ThemeUpdateSerializer

    def patch(self, request):
        store = self.my_store()
        if not store:
            return Response({"detail": "No store yet."}, status=status.HTTP_404_NOT_FOUND)
        theme, _ = StoreTheme.objects.get_or_create(vendor=store)
        serializer = self.get_serializer(theme, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Re-fetch so the serialized theme reflects the just-saved values
        # (the cached store.theme relation would otherwise be stale).
        return Response(VendorDetailSerializer(self.my_store()).data)
