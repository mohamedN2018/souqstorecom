"""Stateless JWT auth + role gates (no local user table)."""
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class StatelessJWTAuthentication(JWTTokenUserAuthentication):
    pass


def token_role(request) -> str:
    return (request.auth or {}).get("role", "") if request.auth else ""


def token_permissions(request) -> list:
    return (request.auth or {}).get("permissions", []) if request.auth else []


def acting_vendor_id(request):
    """The store this request acts for: explicit claim (staff) or own id (owner)."""
    claim = (request.auth or {}).get("vendor_id") if request.auth else None
    return claim or (str(request.user.id) if request.user else None)


class IsVendor(BasePermission):
    """Vendor owners — or store staff who were granted `manage_products`."""

    message = "Vendor (or permitted staff) account required."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = token_role(request)
        if role == "vendor":
            return True
        if role == "staff":
            return "manage_products" in token_permissions(request)
        return False


class IsCustomer(BasePermission):
    message = "Customer account required."

    def has_permission(self, request, view):
        # vendors can buy too, but reviews/checkout are customer-facing
        return bool(request.user and request.user.is_authenticated) and token_role(request) in ("customer", "vendor")
