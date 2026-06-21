from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "role",
            "vendor_id",
            "permissions",
            "is_verified",
            "date_joined",
        )
        read_only_fields = ("id", "role", "vendor_id", "permissions", "is_verified", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )
    # Customers and vendors may self-register; admins/staff are created internally.
    role = serializers.ChoiceField(
        choices=[Role.CUSTOMER, Role.VENDOR], default=Role.CUSTOMER
    )

    class Meta:
        model = User
        fields = ("email", "password", "full_name", "phone", "role")


class StaffSerializer(serializers.ModelSerializer):
    """A staff member as seen by the owner."""

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "permissions", "is_active", "date_joined")


class StaffCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    permissions = serializers.ListField(child=serializers.CharField(), default=list)

    class Meta:
        model = User
        fields = ("email", "password", "full_name", "permissions")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Embed role + identity + store-scoping claims for cross-service checks."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        # vendor_id: who this user acts for in the catalog/store services.
        vid = user.vendor_id or (user.id if user.role == Role.VENDOR else None)
        token["vendor_id"] = str(vid) if vid else None
        token["permissions"] = user.permissions or []
        return token
