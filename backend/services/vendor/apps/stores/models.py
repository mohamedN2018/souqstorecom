import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class VendorStatus(models.TextChoices):
    PENDING = "pending", _("Pending review")
    ACTIVE = "active", _("Active")
    SUSPENDED = "suspended", _("Suspended")


class Vendor(models.Model):
    """A seller storefront within the marketplace."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # owner_id references a User in the Auth service (no cross-service FK).
    owner_id = models.UUIDField(db_index=True)

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    logo_url = models.CharField(max_length=500, blank=True)
    banner_url = models.CharField(max_length=500, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=80, blank=True)

    status = models.CharField(
        max_length=20, choices=VendorStatus.choices, default=VendorStatus.ACTIVE, db_index=True
    )
    is_featured = models.BooleanField(default=False)

    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.PositiveIntegerField(default=0)
    products_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stores_vendor"
        ordering = ("-is_featured", "-rating_avg", "name")

    def __str__(self) -> str:
        return self.name


class StoreTheme(models.Model):
    """
    Per-store visual customization — the 'full custom color' system.
    The frontend reads these and injects them as CSS custom properties.
    """

    LAYOUT_CHOICES = [
        ("classic", "Classic"),
        ("modern", "Modern"),
        ("minimal", "Minimal"),
        ("bold", "Bold"),
    ]

    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name="theme")

    primary_color = models.CharField(max_length=9, default="#2563eb")
    secondary_color = models.CharField(max_length=9, default="#1e293b")
    accent_color = models.CharField(max_length=9, default="#f59e0b")
    background_color = models.CharField(max_length=9, default="#ffffff")
    text_color = models.CharField(max_length=9, default="#0f172a")

    font_family = models.CharField(max_length=80, default="Cairo")
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default="modern")
    rounded = models.PositiveSmallIntegerField(default=12)  # border radius (px)
    dark_mode = models.BooleanField(default=False)

    # extra knobs (banners order, section toggles...) as flexible JSON
    extra = models.JSONField(default=dict, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stores_theme"

    def __str__(self) -> str:
        return f"Theme<{self.vendor.name}>"
