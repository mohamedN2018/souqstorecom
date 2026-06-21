import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Hierarchical product category (self-referencing tree)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    name = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=60, blank=True)  # icon name for the UI
    image_url = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "catalog_category"
        ordering = ("sort_order", "name")
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class ProductStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    ACTIVE = "active", _("Active")
    OUT_OF_STOCK = "out_of_stock", _("Out of stock")
    ARCHIVED = "archived", _("Archived")


class Product(models.Model):
    """A sellable item belonging to a vendor (cross-service by vendor_id)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_id = models.UUIDField(db_index=True)  # -> Vendor service
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=120, blank=True)

    currency = models.CharField(max_length=3, default="EGP")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=ProductStatus.choices, default=ProductStatus.ACTIVE,
        db_index=True,
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    tags = models.JSONField(default=list, blank=True)

    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_product"
        ordering = ("-is_featured", "-created_at")
        indexes = [
            models.Index(fields=["vendor_id", "status"]),
            models.Index(fields=["category", "status"]),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def discount_percent(self) -> int:
        if self.compare_at_price and self.compare_at_price > self.price:
            return round((1 - self.price / self.compare_at_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    url = models.CharField(max_length=500)
    alt = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "catalog_product_image"
        ordering = ("-is_primary", "sort_order")


class ProductVariant(models.Model):
    """A purchasable variation (color/size/...) with its own SKU, price & stock."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=64, unique=True)
    # e.g. {"color": "أحمر", "size": "L"}
    attributes = models.JSONField(default=dict, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "catalog_product_variant"
        ordering = ("-is_default",)


class Purchase(models.Model):
    """
    Record that a customer actually bought a product. Gates reviews so only
    real buyers can rate ("verified purchase"). This is a lightweight stand-in
    for the future Order service — same idea, recorded at checkout.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    customer_id = models.UUIDField(db_index=True)
    qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_purchase"
        constraints = [
            models.UniqueConstraint(fields=["product", "customer_id"], name="uniq_purchase")
        ]


class Review(models.Model):
    """Customer review (customer_id -> Auth service, no FK)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    customer_id = models.UUIDField(db_index=True)
    customer_name = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)  # 1..5
    title = models.CharField(max_length=160, blank=True)
    body = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_review"
        ordering = ("-created_at",)
