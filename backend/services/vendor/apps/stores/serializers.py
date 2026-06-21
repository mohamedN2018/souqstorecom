from rest_framework import serializers

from .models import StoreTheme, Vendor


class StoreThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTheme
        exclude = ("id", "vendor")


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "id",
            "name",
            "slug",
            "tagline",
            "logo_url",
            "banner_url",
            "city",
            "country",
            "status",
            "is_featured",
            "rating_avg",
            "rating_count",
            "products_count",
        )


class VendorDetailSerializer(serializers.ModelSerializer):
    theme = StoreThemeSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = "__all__"
