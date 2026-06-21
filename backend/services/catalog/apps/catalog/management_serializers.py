from django.utils.text import slugify
from rest_framework import serializers

from .models import Category, Product


class ProductWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            "id", "slug", "category_id", "name", "short_description", "description",
            "brand", "currency", "price", "compare_at_price", "status",
            "is_featured", "tags",
        )
        read_only_fields = ("id", "slug")

    def create(self, validated_data):
        name = validated_data["name"]
        base = slugify(name, allow_unicode=True) or "product"
        slug, i = base, 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base}-{i}"
            i += 1
        validated_data["slug"] = slug
        validated_data["vendor_id"] = self.context["vendor_id"]
        return super().create(validated_data)
