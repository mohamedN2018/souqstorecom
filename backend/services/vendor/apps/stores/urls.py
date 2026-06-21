from django.urls import path

from .admin_views import (
    AdminStatsView,
    ApplicationsView,
    ApproveView,
    RejectView,
)
from .management_views import MyStoreView, MyThemeView, VendorRegisterView
from .views import HealthView, VendorDetailView, VendorListView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    # authenticated store-owner endpoints (must precede the <slug> route)
    path("register/", VendorRegisterView.as_view(), name="vendor-register"),
    path("me/", MyStoreView.as_view(), name="vendor-me"),
    path("me/theme/", MyThemeView.as_view(), name="vendor-me-theme"),
    # platform-admin endpoints
    path("admin/applications/", ApplicationsView.as_view(), name="admin-applications"),
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
    path("admin/<uuid:id>/approve/", ApproveView.as_view(), name="admin-approve"),
    path("admin/<uuid:id>/reject/", RejectView.as_view(), name="admin-reject"),
    # public
    path("", VendorListView.as_view(), name="vendor-list"),
    path("<slug:slug>/", VendorDetailView.as_view(), name="vendor-detail"),
]
