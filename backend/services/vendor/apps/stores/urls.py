from django.urls import path

from .views import HealthView, VendorDetailView, VendorListView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("", VendorListView.as_view(), name="vendor-list"),
    path("<slug:slug>/", VendorDetailView.as_view(), name="vendor-detail"),
]
