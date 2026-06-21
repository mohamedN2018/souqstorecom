from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .staff_views import StaffDetailView, StaffListCreateView
from .views import HealthView, LoginView, MeView, RegisterView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("me/", MeView.as_view(), name="me"),
    # store staff management (owner only)
    path("staff/", StaffListCreateView.as_view(), name="staff-list"),
    path("staff/<uuid:id>/", StaffDetailView.as_view(), name="staff-detail"),
]
