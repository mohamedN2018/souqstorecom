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
            "is_verified",
            "date_joined",
        )
        read_only_fields = ("id", "is_verified", "date_joined")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8, validators=[validate_password]
    )
    # Customers and vendors may self-register; admins are created internally.
    role = serializers.ChoiceField(
        choices=[Role.CUSTOMER, Role.VENDOR], default=Role.CUSTOMER
    )

    class Meta:
        model = User
        fields = ("email", "password", "full_name", "phone", "role")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Embed role + identity claims in the access token for cross-service checks."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        return token
