"""
Stateless auth helpers for a service that has no local user table.

The JWT is issued by the Auth service and signed with the shared key. Here we
only read its claims (user_id, role) — no DB lookup — via SimpleJWT's
JWTTokenUserAuthentication. Permissions below gate by the `role` claim.
"""
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class StatelessJWTAuthentication(JWTTokenUserAuthentication):
    """Returns a TokenUser built from claims; never touches a users table."""


def token_role(request) -> str:
    return (request.auth or {}).get("role", "") if request.auth else ""


class IsVendor(BasePermission):
    message = "Vendor account required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and token_role(request) == "vendor"


class IsAdmin(BasePermission):
    message = "Platform admin account required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and token_role(request) == "admin"
