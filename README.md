# 🛒 SouqStore — Marketplace (Microservices)

منصة سوق إلكتروني متعدد البائعين (Marketplace) — معمارية Microservices · Django · Vue · Docker.

> 📐 الخطة المعمارية الكاملة: [docs/PLAN.md](docs/PLAN.md)

---

## التشغيل السريع (Quickstart)

المتطلبات: **Docker + Docker Compose**.

```bash
cp .env.example .env          # عدّل المفاتيح قبل الإنتاج
docker compose up --build     # يشغّل: gateway + auth + postgres + redis + rabbitmq
```

كل شيء يدخل عبر الـ Gateway على المنفذ **8080**.

### تشغيل البنية الكاملة (مع Meilisearch + MinIO)
```bash
docker compose --profile full up --build
```

---

## الخدمات الحالية

| الخدمة | الوصف | المنفذ |
|--------|-------|--------|
| **gateway** | Nginx — مدخل موحّد + توجيه + rate-limit + خدمة `/media/` | `8080` |
| **auth** | Django — تسجيل · JWT · أدوار (customer/vendor/admin) | داخلي `8000` |
| **vendor** | Django — البائعين + المتاجر + الثيم/الألوان | داخلي `8000` |
| **catalog** | Django — الفئات · المنتجات · variants · الصور · التقييمات | داخلي `8000` |
| **auth-db / vendor-db / catalog-db** | PostgreSQL (DB لكل خدمة) | داخلي `5432` |
| **redis** | كاش / sessions / broker | داخلي `6379` |
| **rabbitmq** | Event Bus (+ لوحة إدارة) | `15672` |

> كل الصور تُولَّد محلياً (Pillow) داخل حجم `media-data` ويخدمها الـ gateway على `/media/` — **لا اعتماد على أي خدمة خارجية أو CDN**.

---

## تعبئة بيانات ضخمة (Seed)

بعد `docker compose up`، شغّل البذور (الترتيب مهم):

```bash
docker compose exec auth    python manage.py seed --customers 200 --vendors 24
docker compose exec vendor  python manage.py seed --vendors 24
docker compose exec catalog python manage.py seed --products 1000 --vendors 24
```

ينتج: **200 عميل + 24 بائع + admin · 1000 منتج · ~2400 variant · ~2400 صورة محلية · ~3600 تقييم · 44 فئة**.

- حسابات تجريبية: `admin@souq.test / Admin12345` · `vendor1@souq.test` · `customer1@souq.test` (كلمة السر للجميع: `Password123`).
- معرّفات البائعين تُشتق بنفس الخوارزمية في خدمتي vendor و catalog (uuid5)، فكل منتج يشير لبائع حقيقي **بدون أي نداء بين الخدمات**.

---

## نقاط النهاية — Auth (عبر الـ Gateway)

البادئة: `http://localhost:8080/api/v1/auth/`

| Method | المسار | الوصف |
|--------|--------|-------|
| GET  | `/health/` | فحص حياة الخدمة |
| POST | `/register/` | تسجيل عميل/بائع |
| POST | `/login/` | إصدار access + refresh JWT |
| POST | `/token/refresh/` | تجديد التوكن |
| POST | `/token/verify/` | التحقق من التوكن |
| GET/PATCH | `/me/` | المستخدم الحالي (يتطلب Bearer token) |

توثيق Swagger: `/api/docs/auth/` · `/api/docs/vendor/` · `/api/docs/catalog/`

### نقاط النهاية — Vendor & Catalog (عبر الـ Gateway)

| المسار | الوصف |
|--------|-------|
| `GET /api/v1/vendors/` | قائمة المتاجر (بحث + ترتيب) |
| `GET /api/v1/vendors/<slug>/` | تفاصيل المتجر + الثيم |
| `GET /api/v1/catalog/categories/` | شجرة الفئات |
| `GET /api/v1/catalog/products/` | المنتجات (فلترة: `category`, `vendor`, `min_price`, `max_price`, `min_rating`, `featured`, `search`, `ordering`) |
| `GET /api/v1/catalog/products/<slug>/` | تفاصيل المنتج + variants + صور + تقييمات |

### مثال
```bash
# تسجيل
curl -X POST http://localhost:8080/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"vendor1@souq.test","password":"StrongPass123","role":"vendor"}'

# دخول
curl -X POST http://localhost:8080/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"vendor1@souq.test","password":"StrongPass123"}'
```

---

## بنية المشروع

```
souqstorecom/
├── docker-compose.yml        # الـ stack الكامل
├── .env.example              # إعدادات البيئة
├── gateway/nginx.conf        # توجيه الـ API Gateway
├── services/
│   └── auth/                 # خدمة Auth (Django + DRF + JWT)
│       ├── config/           # إعدادات مشروع Django
│       └── apps/accounts/    # models · services · serializers · views
├── frontend/                 # (قادم) storefront · vendor · admin
└── docs/PLAN.md              # الخطة المعمارية
```

### نمط الكود في كل خدمة
- `models.py` — النماذج · `services.py` — منطق الكتابة · `selectors.py` — منطق القراءة
- `serializers.py` — التحقق/التحويل · `views.py` — طبقة API رفيعة

---

## الخطوة التالية

الخدمة الجاية حسب [docs/PLAN.md](docs/PLAN.md): **Vendor/Store** (ملفات البائعين + إعدادات الثيم)، ثم **Catalog**.
أضف الخدمة الجديدة بنفس قالب `services/auth`، وسجّل مسارها في `gateway/nginx.conf` و `docker-compose.yml`.
