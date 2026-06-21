"""
Seed the Vendor service with realistic stores + themes.

Vendor IDs are derived deterministically (see apps/stores/ids.py) so the
Catalog service can reference them without any cross-service call. Fully offline.

    python manage.py seed --vendors 24
"""
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from faker import Faker

from apps.stores.ids import vendor_id
from apps.stores.models import StoreTheme, Vendor

fake = Faker(["ar_AA", "en_US"])

# Curated bilingual store names for believable demo data.
STORE_NAMES = [
    ("سوق الإلكترونيات", "Electronics Souq"),
    ("بيت الأزياء", "Fashion House"),
    ("ركن الجمال", "Beauty Corner"),
    ("عالم الأطفال", "Kids World"),
    ("مملكة المنزل", "Home Kingdom"),
    ("متجر الرياضة", "Sports Store"),
    ("واحة الكتب", "Books Oasis"),
    ("جوهرة المجوهرات", "Jewel Gallery"),
    ("تك ستور", "Tech Store"),
    ("الذواقة للأطعمة", "Gourmet Foods"),
    ("ركن الهدايا", "Gift Nook"),
    ("أناقة الساعات", "Watch Elegance"),
    ("بازار العطور", "Perfume Bazaar"),
    ("حديقة النباتات", "Plant Garden"),
    ("استوديو الفن", "Art Studio"),
    ("عالم الألعاب", "Toy Planet"),
    ("متجر السيارات", "Auto Parts Hub"),
    ("صحة وعافية", "Health & Wellness"),
    ("ركن القهوة", "Coffee Corner"),
    ("ديكور الفخامة", "Luxe Decor"),
    ("موبايل بلس", "Mobile Plus"),
    ("أحذية المدينة", "City Shoes"),
    ("حقائب أنيقة", "Chic Bags"),
    ("نور للإضاءة", "Noor Lighting"),
    ("مزرعة العسل", "Honey Farm"),
    ("خيمة التوابل", "Spice Tent"),
]

PALETTES = [
    ("#2563eb", "#1e293b", "#f59e0b"),
    ("#16a34a", "#14532d", "#facc15"),
    ("#db2777", "#831843", "#22d3ee"),
    ("#9333ea", "#3b0764", "#f97316"),
    ("#dc2626", "#450a0a", "#fbbf24"),
    ("#0891b2", "#083344", "#f43f5e"),
    ("#ea580c", "#431407", "#10b981"),
    ("#4f46e5", "#1e1b4b", "#ec4899"),
]
FONTS = ["Cairo", "Tajawal", "Almarai", "IBM Plex Sans Arabic", "Changa"]
CITIES = ["القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "أسيوط", "طنطا", "الزقازيق"]


class Command(BaseCommand):
    help = "Seed vendors and store themes"

    def add_arguments(self, parser):
        parser.add_argument("--vendors", type=int, default=24)

    @transaction.atomic
    def handle(self, *args, **opts):
        count = opts["vendors"]
        random.seed(42)

        Vendor.objects.all().delete()
        created = 0

        for i in range(count):
            ar, en = STORE_NAMES[i % len(STORE_NAMES)]
            if i >= len(STORE_NAMES):
                en = f"{en} {i // len(STORE_NAMES) + 1}"
                ar = f"{ar} {i // len(STORE_NAMES) + 1}"

            primary, secondary, accent = random.choice(PALETTES)
            vendor = Vendor.objects.create(
                id=vendor_id(i),
                owner_id=vendor_id(i),  # demo: owner mirrors vendor id
                name=ar,
                slug=slugify(en) or f"store-{i}",
                tagline=random.choice(
                    ["جودة تستحق الثقة", "أفضل الأسعار", "تسوق بثقة", "منتجات أصلية 100%"]
                ),
                description=fake["ar_AA"].paragraph(nb_sentences=5),
                logo_url=f"/media/vendors/logo_{i % 12}.jpg",
                banner_url=f"/media/vendors/banner_{i % 8}.jpg",
                email=fake["en_US"].company_email(),
                phone=f"+201{random.randint(0,2)}{random.randint(10**7, 10**8 - 1)}",
                country="مصر",
                city=random.choice(CITIES),
                is_featured=(i < 6),
                rating_avg=round(random.uniform(3.6, 5.0), 2),
                rating_count=random.randint(12, 4200),
                products_count=0,  # updated by catalog seeder reporting, kept simple here
            )
            StoreTheme.objects.create(
                vendor=vendor,
                primary_color=primary,
                secondary_color=secondary,
                accent_color=accent,
                font_family=random.choice(FONTS),
                layout=random.choice(["classic", "modern", "minimal", "bold"]),
                rounded=random.choice([6, 8, 12, 16, 24]),
                dark_mode=random.random() < 0.2,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"[vendor] seeded {created} vendors + themes"))
