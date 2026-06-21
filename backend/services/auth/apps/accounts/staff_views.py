"""Vendor-owner manages their store staff (sub-accounts with scoped permissions)."""
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import STAFF_PERMISSIONS, Role
from .serializers import StaffCreateSerializer, StaffSerializer

User = get_user_model()


class IsVendorOwner(BasePermission):
    message = "Vendor owner account required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and request.user.role == Role.VENDOR


class StaffListCreateView(generics.ListCreateAPIView):
    """GET (my staff) / POST (create staff) — /api/v1/auth/staff/"""

    permission_classes = [IsVendorOwner]

    def get_serializer_class(self):
        return StaffCreateSerializer if self.request.method == "POST" else StaffSerializer

    def get_queryset(self):
        return User.objects.filter(role=Role.STAFF, vendor_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        perms = [p for p in data.get("permissions", []) if p in STAFF_PERMISSIONS]
        try:
            staff = User.objects.create_user(
                email=data["email"],
                password=data["password"],
                full_name=data.get("full_name", ""),
                role=Role.STAFF,
                vendor_id=request.user.id,   # works under this owner's store
                permissions=perms,
                is_verified=True,
            )
        except IntegrityError:
            return Response({"email": ["مستخدم بهذا البريد موجود بالفعل."]}, status=status.HTTP_409_CONFLICT)
        return Response(StaffSerializer(staff).data, status=status.HTTP_201_CREATED)


class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    """PATCH (update permissions) / DELETE — /api/v1/auth/staff/<id>/"""

    permission_classes = [IsVendorOwner]
    serializer_class = StaffSerializer
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.filter(role=Role.STAFF, vendor_id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        staff = self.get_object()
        if "permissions" in request.data:
            staff.permissions = [p for p in request.data["permissions"] if p in STAFF_PERMISSIONS]
        if "is_active" in request.data:
            staff.is_active = bool(request.data["is_active"])
        staff.save(update_fields=["permissions", "is_active"])
        return Response(StaffSerializer(staff).data)
