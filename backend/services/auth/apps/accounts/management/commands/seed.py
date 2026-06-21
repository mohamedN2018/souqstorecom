"""
Seed the Auth service with demo accounts (no external deps).

    python manage.py seed --customers 200 --vendors 24

- Vendor user IDs are derived with the same deterministic scheme as the
  Vendor service (vendor_id(i)), so a vendor account maps to its store.
- One admin superuser: admin@souq.test / Admin12345
- All demo passwords: Password123
"""
import uuid

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

User = get_user_model()

VENDOR_NAMESPACE = uuid.UUID("11111111-1111-1111-1111-111111111111")
DEMO_PASSWORD = "Password123"

FIRST = ["أحمد", "محمد", "محمود", "سارة", "منى", "يوسف", "نور", "كريم", "هبة", "عمر",
         "ريم", "خالد", "ليلى", "طارق", "دينا", "حسن", "مريم", "علي", "فاطمة", "زياد"]
LAST = ["علي", "حسن", "إبراهيم", "خالد", "عبدالله", "سامي", "فؤاد", "مصطفى", "ناصر", "السيد"]


def vendor_id(index: int) -> uuid.UUID:
    return uuid.uuid5(VENDOR_NAMESPACE, f"vendor:{index}")


def applicant_id(index: int) -> uuid.UUID:
    return uuid.uuid5(VENDOR_NAMESPACE, f"applicant:{index}")


class Command(BaseCommand):
    help = "Seed demo users (customers, vendors, admin)"

    def add_arguments(self, parser):
        parser.add_argument("--customers", type=int, default=200)
        parser.add_argument("--vendors", type=int, default=60)

    @transaction.atomic
    def handle(self, *args, **opts):
        n_customers = opts["customers"]
        n_vendors = opts["vendors"]

        User.objects.exclude(is_superuser=True).delete()

        # admin
        if not User.objects.filter(email="admin@souq.test").exists():
            User.objects.create_superuser(
                email="admin@souq.test", password="Admin12345", full_name="مدير المنصة"
            )
            self.stdout.write("  + admin@souq.test / Admin12345")

        hashed = None
        vendors = []
        for i in range(n_vendors):
            u = User(
                id=vendor_id(i),
                email=f"vendor{i+1}@souq.test",
                full_name=f"بائع رقم {i+1}",
                role="vendor",
                is_verified=True,
            )
            u.set_password(DEMO_PASSWORD)
            hashed = u.password  # reuse the same hash for speed on demo customers
            vendors.append(u)
        User.objects.bulk_create(vendors, batch_size=500)

        customers = []
        for i in range(n_customers):
            full = f"{FIRST[i % len(FIRST)]} {LAST[(i // len(FIRST)) % len(LAST)]}"
            customers.append(User(
                email=f"customer{i+1}@souq.test",
                full_name=full,
                role="customer",
                is_verified=(i % 3 == 0),
                password=hashed,  # all demo customers share Password123
            ))
        User.objects.bulk_create(customers, batch_size=1000)

        # --- pending vendor applicants (await admin approval in vendor service) ---
        applicants = []
        for i in range(2):
            u = User(
                id=applicant_id(i),
                email=f"applicant{i+1}@souq.test",
                full_name=f"مقدّم طلب متجر {i+1}",
                role="vendor",
                is_verified=True,
                password=hashed,
            )
            applicants.append(u)
        User.objects.bulk_create(applicants)

        # --- demo staff member under vendor1's store (scoped permissions) ---
        staff = User(
            email="staff1@souq.test",
            full_name="موظف متجر",
            role="staff",
            vendor_id=vendor_id(0),  # works for vendor1's store
            permissions=["manage_products", "view_analytics"],
            is_verified=True,
            password=hashed,
        )
        staff.save()

        self.stdout.write(self.style.SUCCESS(
            f"[auth] seeded {n_vendors} vendors + {n_customers} customers + 2 applicants "
            f"+ 1 staff (+admin). Password for all: {DEMO_PASSWORD}"
        ))
