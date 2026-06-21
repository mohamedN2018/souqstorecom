"""
Seed the Catalog service with a large, detailed, fully-offline dataset.

    python manage.py seed --products 1000 --vendors 24

Generates: hierarchical categories, products (with variants, locally-rendered
images, tags, ratings) and customer reviews. Product `vendor_id`s are derived
with the same deterministic scheme as the Vendor service, so every product
points at a real store — with zero cross-service calls.
"""
import random
import uuid
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from faker import Faker

from apps.catalog import data
from apps.catalog.imagegen import generate_pool, make_image
from apps.catalog.models import (
    Category,
    Product,
    ProductImage,
    ProductStatus,
    ProductVariant,
    Review,
)

fake = Faker(["ar_AA"])

# Must match the Vendor service (apps/stores/ids.py).
VENDOR_NAMESPACE = uuid.UUID("11111111-1111-1111-1111-111111111111")


def vendor_id(index: int) -> uuid.UUID:
    return uuid.uuid5(VENDOR_NAMESPACE, f"vendor:{index}")


class Command(BaseCommand):
    help = "Seed categories, products, variants, images and reviews"

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=4000)
        parser.add_argument("--vendors", type=int, default=60)

    @transaction.atomic
    def handle(self, *args, **opts):
        n_products = opts["products"]
        n_vendors = opts["vendors"]
        rnd = random.Random(7)
        media_root = str(settings.MEDIA_ROOT)

        self.stdout.write("[catalog] clearing old data ...")
        Review.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # ----- 1) categories (top + subs) -----
        self.stdout.write("[catalog] creating categories ...")
        top_cats, sub_cats = [], []
        for order, (ar_name, meta) in enumerate(data.CATEGORY_TREE.items()):
            top = Category.objects.create(
                name=ar_name, name_en=meta["en"], icon=meta["icon"],
                slug=slugify(meta["en"]), sort_order=order,
            )
            top_cats.append((top, meta))
            for s_order, sub in enumerate(meta["subs"]):
                sub_obj = Category.objects.create(
                    parent=top, name=sub, name_en=f"{meta['en']} - {sub}",
                    icon=meta["icon"],
                    slug=f"{slugify(meta['en'])}-{s_order}", sort_order=s_order,
                )
                sub_cats.append((sub_obj, meta))

        # ----- 2) local image pools (per top category) + vendor media -----
        self.stdout.write("[catalog] generating local images (Pillow) ...")
        labels = [m["en"] for _, m in top_cats]
        pools = generate_pool(media_root, "products", labels, per_label=8)
        for i in range(12):
            make_image(f"{media_root}/vendors/logo_{i}.jpg", "Store", seed=900 + i, size=(300, 300))
        for i in range(8):
            make_image(f"{media_root}/vendors/banner_{i}.jpg", "SouqStore", seed=950 + i, size=(1200, 360))

        # ----- 3) products + children (bulk) -----
        self.stdout.write(f"[catalog] building {n_products} products ...")
        products, images, variants, reviews = [], [], [], []

        for p in range(n_products):
            sub_obj, meta = rnd.choice(sub_cats)
            ptype = rnd.choice(meta["types"])
            brand = rnd.choice(meta["brands"])
            desc = rnd.choice(data.DESCRIPTORS)
            name = f"{ptype} {brand} {desc}"
            slug = f"{slugify(name, allow_unicode=False) or 'product'}-{p}"

            base = Decimal(rnd.randrange(50, 45000))
            has_discount = rnd.random() < 0.55
            compare = (base * Decimal("1.25")).quantize(Decimal("1")) if has_discount else None
            v_idx = rnd.randrange(n_vendors)

            n_reviews = rnd.choices([0, 1, 2, 3, 5, 8, 14], weights=[6, 8, 10, 10, 8, 5, 3])[0]
            ratings = [rnd.choices([3, 4, 5], weights=[1, 3, 6])[0] for _ in range(n_reviews)]
            rating_avg = round(sum(ratings) / len(ratings), 2) if ratings else 0
            label = meta["en"]

            product = Product(
                vendor_id=vendor_id(v_idx),
                category=sub_obj,
                name=name,
                slug=slug,
                short_description=f"{ptype} {brand} بخامة ممتازة وضمان.",
                description=fake.paragraph(nb_sentences=6),
                brand=brand,
                currency="EGP",
                price=base,
                compare_at_price=compare,
                status=rnd.choices(
                    [ProductStatus.ACTIVE, ProductStatus.OUT_OF_STOCK],
                    weights=[9, 1],
                )[0],
                is_featured=(rnd.random() < 0.12),
                tags=rnd.sample([brand, ptype, "عرض", "جديد", "الأكثر مبيعاً"], k=2),
                rating_avg=rating_avg,
                rating_count=len(ratings),
                sold_count=rnd.randrange(0, 5000),
                views_count=rnd.randrange(0, 30000),
            )
            products.append(product)

            # images (1..4 from the category pool)
            pool = pools[label]
            for n in range(rnd.randint(1, 4)):
                images.append(ProductImage(
                    product=product, url=rnd.choice(pool),
                    alt=name, is_primary=(n == 0), sort_order=n,
                ))

            # variants (1..4)
            n_var = rnd.randint(1, 4)
            for v in range(n_var):
                attrs = {"اللون": rnd.choice(data.COLORS)}
                if meta["en"] in ("Men Fashion", "Women Fashion", "Sports & Fitness"):
                    attrs["المقاس"] = rnd.choice(data.SIZES)
                variants.append(ProductVariant(
                    product=product,
                    sku=f"SKU-{p}-{v}",
                    attributes=attrs,
                    price=base + Decimal(rnd.randrange(0, 500)),
                    compare_at_price=compare,
                    stock=rnd.randrange(0, 250),
                    is_default=(v == 0),
                ))

            # reviews
            for r, rating in enumerate(ratings):
                reviews.append(Review(
                    product=product,
                    customer_id=uuid.uuid4(),
                    customer_name=rnd.choice(data.CUSTOMER_NAMES),
                    rating=rating,
                    title=rnd.choice(data.REVIEW_TITLES),
                    body=rnd.choice(data.REVIEW_BODIES),
                    is_verified_purchase=(rnd.random() < 0.7),
                ))

        self.stdout.write("[catalog] writing to database (bulk) ...")
        Product.objects.bulk_create(products, batch_size=500)
        ProductImage.objects.bulk_create(images, batch_size=1000)
        ProductVariant.objects.bulk_create(variants, batch_size=1000)
        Review.objects.bulk_create(reviews, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(
            f"[catalog] done: {len(products)} products, {len(variants)} variants, "
            f"{len(images)} images, {len(reviews)} reviews, "
            f"{len(top_cats)} top + {len(sub_cats)} sub categories."
        ))
