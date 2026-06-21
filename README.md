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
| **gateway** | Nginx — مدخل موحّد + توجيه + rate-limit | `8080` |
| **auth** | Django — تسجيل · JWT · أدوار (customer/vendor/admin) | داخلي `8000` |
| **auth-db** | PostgreSQL (خاص بخدمة auth) | داخلي `5432` |
| **redis** | كاش / sessions / broker | داخلي `6379` |
| **rabbitmq** | Event Bus (+ لوحة إدارة) | `15672` |

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

توثيق Swagger للخدمة: `http://localhost:8080/api/docs/auth/`

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
