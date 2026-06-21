from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from . import services
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.GenericAPIView):
    """POST /api/v1/auth/register/ — create a customer or vendor account."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = services.register_user(**serializer.validated_data)
        except IntegrityError:
            return Response(
                {"email": ["A user with this email already exists."]},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """POST /api/v1/auth/login/ — returns access + refresh JWT."""

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/v1/auth/me/ — current authenticated user."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class HealthView(APIView):
    """GET /api/v1/auth/health/ — liveness probe for the gateway/orchestrator."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "service": "auth"})
