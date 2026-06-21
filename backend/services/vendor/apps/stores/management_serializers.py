from rest_framework import serializers

from .models import StoreTheme, Vendor


class VendorRegisterSerializer(serializers.ModelSerializer):
    terms_accepted = serializers.BooleanField()

    class Meta:
        model = Vendor
        fields = ("name", "tagline", "description", "email", "phone", "country", "city", "terms_accepted")

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError("يجب الموافقة على شروط المنصة.")
        return value


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "name", "tagline", "description", "logo_url", "banner_url",
            "email", "phone", "country", "city",
        )


class ThemeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTheme
        fields = (
            "primary_color", "secondary_color", "accent_color",
            "background_color", "text_color", "font_family", "layout",
            "rounded", "dark_mode", "extra",
        )
