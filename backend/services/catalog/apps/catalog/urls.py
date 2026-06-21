from django.urls import path

from .management_views import MyProductDetailView, MyProductsView
from .review_views import CheckoutView, ProductReviewView
from .views import (
    CategoryListView,
    HealthView,
    ProductDetailView,
    ProductListView,
)

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # vendor product management (auth: role=vendor)
    path("manage/products/", MyProductsView.as_view(), name="manage-products"),
    path("manage/products/<uuid:id>/", MyProductDetailView.as_view(), name="manage-product"),

    # checkout + verified-purchase reviews (auth: customer)
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("products/<slug:slug>/reviews/", ProductReviewView.as_view(), name="product-reviews"),

    # public browsing
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
