from rest_framework import filters, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vendor
from .serializers import VendorDetailSerializer, VendorListSerializer


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "vendor"})


class VendorListView(generics.ListAPIView):
    """GET /api/v1/vendors/ — browse stores (search + ordering)."""

    queryset = Vendor.objects.all()
    serializer_class = VendorListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "tagline", "city"]
    ordering_fields = ["rating_avg", "products_count", "created_at"]


class VendorDetailView(generics.RetrieveAPIView):
    """GET /api/v1/vendors/<slug>/ — store profile + theme."""

    queryset = Vendor.objects.select_related("theme")
    serializer_class = VendorDetailSerializer
    lookup_field = "slug"
