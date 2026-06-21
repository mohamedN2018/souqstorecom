from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "catalog"})


class CategoryListView(generics.ListAPIView):
    """GET /api/v1/catalog/categories/ — full category tree (flat)."""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None
    search_fields = ["name", "name_en"]


class ProductListView(generics.ListAPIView):
    """GET /api/v1/catalog/products/ — filter, search, sort, paginate."""

    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    search_fields = ["name", "brand", "short_description"]
    ordering_fields = ["price", "rating_avg", "sold_count", "created_at"]

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.all())
        ).select_related("category")


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/v1/catalog/products/<slug>/ — full product detail."""

    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.select_related("category").prefetch_related(
            "images", "variants", "reviews"
        )
