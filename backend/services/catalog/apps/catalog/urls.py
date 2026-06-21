from django.urls import path

from .views import (
    CategoryListView,
    HealthView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
