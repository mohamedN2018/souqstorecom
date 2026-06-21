"""Platform-admin endpoints: review and approve/reject vendor applications + stats."""
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SiteSettings, Vendor, VendorStatus
from .permissions import IsAdmin, StatelessJWTAuthentication
from .serializers import VendorDetailSerializer, VendorListSerializer


class AdminBase:
    authentication_classes = [StatelessJWTAuthentication]
    permission_classes = [IsAdmin]


class ApplicationsView(AdminBase, generics.ListAPIView):
    """GET /api/v1/vendors/admin/applications/?status=pending"""

    serializer_class = VendorListSerializer

    def get_queryset(self):
        qs = Vendor.objects.all().order_by("-created_at")
        status_q = self.request.query_params.get("status")
        return qs.filter(status=status_q) if status_q else qs


class ApproveView(AdminBase, GenericAPIView):
    """POST /api/v1/vendors/admin/<id>/approve/"""

    def post(self, request, id):
        vendor = Vendor.objects.filter(id=id).first()
        if not vendor:
            return Response({"detail": "Not found"}, status=404)
        vendor.status = VendorStatus.ACTIVE
        vendor.rejection_reason = ""
        vendor.reviewed_at = timezone.now()
        vendor.save(update_fields=["status", "rejection_reason", "reviewed_at"])
        return Response(VendorDetailSerializer(vendor).data)


class RejectView(AdminBase, GenericAPIView):
    """POST /api/v1/vendors/admin/<id>/reject/  body: { reason }"""

    def post(self, request, id):
        vendor = Vendor.objects.filter(id=id).first()
        if not vendor:
            return Response({"detail": "Not found"}, status=404)
        vendor.status = VendorStatus.SUSPENDED
        vendor.rejection_reason = request.data.get("reason", "")
        vendor.reviewed_at = timezone.now()
        vendor.save(update_fields=["status", "rejection_reason", "reviewed_at"])
        return Response(VendorDetailSerializer(vendor).data)


class AdminStatsView(AdminBase, APIView):
    """GET /api/v1/vendors/admin/stats/ — platform overview."""

    def get(self, request):
        return Response({
            "vendors_total": Vendor.objects.count(),
            "vendors_active": Vendor.objects.filter(status=VendorStatus.ACTIVE).count(),
            "vendors_pending": Vendor.objects.filter(status=VendorStatus.PENDING).count(),
            "vendors_suspended": Vendor.objects.filter(status=VendorStatus.SUSPENDED).count(),
        })


class SiteSettingsView(GenericAPIView):
    """
    GET  /api/v1/site/settings/  — public (storefront reads the global theme)
    PATCH /api/v1/site/settings/ — admin only (edit global theme + terms)
    """

    authentication_classes = [StatelessJWTAuthentication]

    def get_permissions(self):
        return [IsAdmin()] if self.request.method == "PATCH" else []

    def _data(self, s):
        return {
            "site_name": s.site_name,
            "primary_color": s.primary_color,
            "secondary_color": s.secondary_color,
            "accent_color": s.accent_color,
            "rounded": s.rounded,
            "announcement": s.announcement,
            "vendor_terms": s.vendor_terms,
        }

    def get(self, request):
        return Response(self._data(SiteSettings.load()))

    def patch(self, request):
        s = SiteSettings.load()
        for f in ("site_name", "primary_color", "secondary_color", "accent_color",
                  "rounded", "announcement", "vendor_terms"):
            if f in request.data:
                setattr(s, f, request.data[f])
        s.save()
        return Response(self._data(s))
