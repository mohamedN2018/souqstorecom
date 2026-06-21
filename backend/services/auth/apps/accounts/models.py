import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class Role(models.TextChoices):
    CUSTOMER = "customer", _("Customer")
    VENDOR = "vendor", _("Vendor")
    STAFF = "staff", _("Store staff")
    ADMIN = "admin", _("Admin")


# Permission keys a vendor owner may grant to a staff member.
STAFF_PERMISSIONS = [
    "manage_products",   # add/edit/delete products
    "view_orders",       # see store orders
    "manage_theme",      # edit store appearance
    "view_analytics",    # see store stats
]


class User(AbstractBaseUser, PermissionsMixin):
    """
    Email-based user for the marketplace.

    A single account can act as a customer and/or vendor; `role` marks the
    primary capability and is embedded in the JWT for cross-service checks.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    phone = models.CharField(_("phone"), max_length=32, blank=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.CUSTOMER, db_index=True
    )

    # For staff: the owner (vendor) user id they work for. For vendor owners it
    # may mirror their own id. Embedded in the JWT so other services can scope
    # actions to the right store without a cross-service lookup.
    vendor_id = models.UUIDField(null=True, blank=True, db_index=True)
    # Granted capability keys (see STAFF_PERMISSIONS). Empty for owners (full).
    permissions = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "accounts_user"
        ordering = ("-date_joined",)

    def __str__(self) -> str:
        return self.email

    @property
    def is_vendor(self) -> bool:
        return self.role == Role.VENDOR

    @property
    def is_customer(self) -> bool:
        return self.role == Role.CUSTOMER
