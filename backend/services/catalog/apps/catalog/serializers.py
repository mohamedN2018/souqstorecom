from rest_framework import serializers

from .models import Category, Product, ProductImage, ProductVariant, Review


class CategorySerializer(serializers.ModelSerializer):
    children_count = serializers.IntegerField(source="children.count", read_only=True)
    products_count = serializers.IntegerField(source="products.count", read_only=True)

    class Meta:
        model = Category
        fields = (
            "id", "parent", "name", "name_en", "slug", "icon",
            "image_url", "sort_order", "children_count", "products_count",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("url", "alt", "is_primary", "sort_order")


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("id", "sku", "attributes", "price", "compare_at_price", "stock", "is_default")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id", "customer_name", "rating", "title", "body",
            "is_verified_purchase", "created_at",
        )


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    discount_percent = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "vendor_id", "name", "slug", "short_description", "brand",
            "currency", "price", "compare_at_price", "discount_percent",
            "status", "is_featured", "rating_avg", "rating_count", "sold_count",
            "primary_image",
        )

    def get_primary_image(self, obj):
        img = next((i for i in obj.images.all() if i.is_primary), None) or (
            obj.images.all()[0] if obj.images.all() else None
        )
        return img.url if img else ""


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    recent_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "vendor_id", "category", "name", "slug",
            "short_description", "description", "brand", "currency",
            "price", "compare_at_price", "discount_percent", "status",
            "is_featured", "tags", "rating_avg", "rating_count", "sold_count",
            "views_count", "images", "variants", "recent_reviews", "created_at",
        )

    def get_recent_reviews(self, obj):
        return ReviewSerializer(obj.reviews.all()[:5], many=True).data
