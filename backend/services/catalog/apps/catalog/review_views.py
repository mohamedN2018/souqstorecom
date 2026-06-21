"""Checkout (records purchases) + verified-purchase reviews."""
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Product, Purchase, Review
from .permissions import IsCustomer, StatelessJWTAuthentication
from .serializers import ReviewSerializer


class CheckoutSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField(), allow_empty=False)


class CheckoutView(GenericAPIView):
    """
    POST /api/v1/catalog/checkout/ — records a purchase per item so the buyer
    can later leave a *verified* review. (Stand-in for the Order service.)
    Body: { "items": [ { "product_id": "...", "qty": 2 }, ... ] }
    """

    authentication_classes = [StatelessJWTAuthentication]
    permission_classes = [IsCustomer]
    serializer_class = CheckoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_id = request.user.id
        recorded = 0
        for item in serializer.validated_data["items"]:
            pid = item.get("product_id")
            if not Product.objects.filter(id=pid).exists():
                continue
            try:
                with transaction.atomic():
                    Purchase.objects.create(
                        product_id=pid, customer_id=customer_id,
                        qty=int(item.get("qty", 1)),
                    )
                    recorded += 1
            except IntegrityError:
                pass  # already purchased — fine
        return Response({"recorded": recorded}, status=status.HTTP_201_CREATED)


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("rating", "title", "body")


class ProductReviewView(GenericAPIView):
    """
    GET  /api/v1/catalog/products/<slug>/reviews/  — list reviews
    POST /api/v1/catalog/products/<slug>/reviews/  — review (verified buyers only)
    """

    serializer_class = ReviewCreateSerializer

    def get_authenticators(self):
        return [StatelessJWTAuthentication()]

    def get_permissions(self):
        return [IsCustomer()] if self.request.method == "POST" else []

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return Response(ReviewSerializer(product.reviews.all()[:50], many=True).data)

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        customer_id = request.user.id

        # ✅ enforce: only customers who actually bought this product may review.
        if not Purchase.objects.filter(product=product, customer_id=customer_id).exists():
            return Response(
                {"detail": "يمكنك تقييم المنتج فقط بعد شرائه."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if Review.objects.filter(product=product, customer_id=customer_id).exists():
            return Response({"detail": "لقد قيّمت هذا المنتج بالفعل."}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(
            product=product,
            customer_id=customer_id,
            customer_name=(request.auth or {}).get("email", "").split("@")[0],
            is_verified_purchase=True,
            **serializer.validated_data,
        )

        # recompute aggregate rating
        agg = product.reviews.aggregate(avg=Avg("rating"), n=Count("id"))
        product.rating_avg = round(agg["avg"] or 0, 2)
        product.rating_count = agg["n"]
        product.save(update_fields=["rating_avg", "rating_count"])

        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
