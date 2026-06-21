# 🛒 SouqStore — Marketplace (Microservices)

منصة سوق إلكتروني متعدد البائعين — **Backend** (Django microservices) + **Frontend** (Vue 3) + Docker.

> 📐 الخطة المعمارية الكاملة: [docs/PLAN.md](docs/PLAN.md)

---

## التشغيل السريع

المتطلبات: **Docker + Docker Compose** فقط (كل الباكدجات داخل الصور — لا شيء خارجي).

```bash
cp .env.example .env
docker compose up --build
```

| الواجهة | الرابط |
|---------|--------|
| 🛍️ المتجر (Vue) | http://localhost:5280 |
| 🔌 API Gateway | http://localhost:18080 |
| 🐰 RabbitMQ console | http://localhost:15673 |

> البورتات مختارة بأرقام غير شائعة (5280 / 18080 / 15673) لتفادي التعارض مع مشاريع أخرى.

---

## بنية المشروع

```
souqstorecom/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── gateway/nginx.conf            # API Gateway (توجيه + rate-limit + /media)
│   └── services/
│       ├── auth/                     # تسجيل · JWT · أدوار
│       ├── vendor/                   # البائعين + المتاجر + الثيم/الألوان
│       └── catalog/                  # الفئات · المنتجات · variants · صور · تقييمات
├── frontend/
│   └── storefront/                   # Vue 3 + Vite + Tailwind + GSAP + i18n (RTL)
└── docs/PLAN.md
```

كل خدمة: `models.py` · `services.py` (كتابة) · `selectors`/`serializers` · `views.py` (API رفيع)، وقاعدة PostgreSQL خاصة بها (DB-per-service).

---

## الواجهة الأمامية (Frontend)

Vue 3 + Vite + Tailwind + GSAP + Pinia + Vue-Router + vue-i18n.

- **RTL/LTR** تبديل عربي/إنجليزي فوري.
- **نظام ألوان كامل (Full Custom):** كل ألوان الواجهة عبارة عن CSS variables، وزر 🎨 (أسفل اليسار) يغيّرها مباشرة (presets + color pickers). صفحة كل متجر تطبّق ثيمه الخاص تلقائياً.
- **GSAP** أنميشن للـ hero والكروت + عدّاد تنازلي للعروض.
- **متجاوب** بالكامل (mobile-first).
- كل الطلبات same-origin عبر بروكسي Vite → الـ gateway (لا CORS، لا روابط خارجية).

الصفحات: الرئيسية · المنتجات (فلترة/بحث/ترتيب/صفحات) · تفاصيل المنتج · المتاجر · صفحة متجر · السلة.

---

## تعبئة بيانات ضخمة (Seed)

```bash
docker compose exec auth    python manage.py seed --customers 200 --vendors 24
docker compose exec vendor  python manage.py seed --vendors 24
docker compose exec catalog python manage.py seed --products 1000 --vendors 24
```

ينتج: **200 عميل + 24 بائع + admin · 1000 منتج · ~2400 variant · ~2400 صورة محلية · ~3600 تقييم · 44 فئة**.

- الصور تُولَّد محلياً بـ Pillow في حجم `media-data` ويخدمها الـ gateway على `/media/` — لا CDN.
- معرّفات البائعين تُشتق بنفس الخوارزمية (uuid5) في خدمتي vendor و catalog → كل منتج يشير لبائع حقيقي بدون نداء بين الخدمات.

حسابات تجريبية: `admin@souq.test / Admin12345` · `vendor1@souq.test` · `customer1@souq.test` (كلمة السر: `Password123`).

---

## نقاط النهاية (عبر الـ Gateway · `http://localhost:18080`)

| المسار | الوصف |
|--------|-------|
| `POST /api/v1/auth/register/ · /login/ · GET /me/` | المصادقة + JWT |
| `GET /api/v1/vendors/ · /<slug>/` | المتاجر + الثيم |
| `GET /api/v1/catalog/categories/` | شجرة الفئات |
| `GET /api/v1/catalog/products/` | فلترة: `category,vendor,min_price,max_price,min_rating,featured,search,ordering` |
| `GET /api/v1/catalog/products/<slug>/` | تفاصيل + variants + صور + تقييمات |

Swagger: `/api/docs/auth/` · `/api/docs/vendor/` · `/api/docs/catalog/`

---

## مزايا تفاعلية (مضافة)

- **تسجيل عميل + تسجيل متجر** (`/login` · `/register` · `/sell`) — JWT.
- **لوحة تحكم البائع** (`/dashboard`): إدارة منتجاته + تحكّم كامل بألوان واجهة متجره (محرّر الألوان انتقل هنا بدل العام).
- **ريل-تايم (WebSocket / Django Channels):** أي منتج يضيفه بائع يظهر **فوراً** في المتجر واللوحة بدون تحديث.
- **تقييمات موثّقة:** فقط من اشترى المنتج فعلاً يقدر يقيّمه (الخادم يفرض ذلك — 403 لغير المشتري).
- **HMR مضبوط:** التعديلات تظهر مباشرة بدون refresh يدوي.

### نقاط نهاية إضافية
| المسار | الصلاحية |
|--------|----------|
| `POST /api/v1/vendors/register/ · GET/PATCH /me/ · PATCH /me/theme/` | بائع (JWT) |
| `GET/POST /api/v1/catalog/manage/products/` · `PATCH/DELETE /manage/products/<id>/` | بائع (JWT) |
| `POST /api/v1/catalog/checkout/` | عميل (JWT) |
| `GET/POST /api/v1/catalog/products/<slug>/reviews/` | تقييم: مشترٍ موثّق فقط |
| `WS /ws/products/` | بث لحظي للمنتجات |

---

## لوحات التحكم والأدوار (RBAC)

لوحات **معزولة تماماً** عن واجهة الموقع (شريط جانبي + هيدر خاص + زر "العودة للموقع").

| الدور | اللوحة | يقدر يعمل |
|------|--------|-----------|
| **مدير المنصة** | `/admin` | مراجعة طلبات المتاجر (موافقة/رفض) · إحصائيات · **ألوان الموقع العامة (هو الوحيد)** · شريط الإعلان · شروط البائعين |
| **صاحب المتجر** | `/dashboard` | إدارة منتجاته (إضافة/**تعديل**/حذف، عرض حديث) · بيانات المتجر · ألوان متجره · **الموظفون + صلاحياتهم** · حالة الطلب |
| **موظف المتجر** | `/dashboard` | فقط ما منحه صاحب المتجر (لوحة مقيّدة بالصلاحيات) |

**سير عمل فتح المتجر:** البائع يقدّم طلب من `/sell` (مع الموافقة على الشروط) → الحالة `pending` → المدير يراجع/يتواصل → يوافق → المتجر يُفعّل ويظهر.

### حسابات تجريبية (كلمة السر `Password123` للجميع عدا الأدمن)
| الحساب | الدور |
|--------|-------|
| `admin@souq.test` / **Admin12345** | مدير المنصة |
| `vendor1@souq.test` | صاحب متجر (مفعّل) |
| `staff1@souq.test` | موظف (إدارة منتجات + إحصائيات) |
| `applicant1@souq.test` | طلب متجر بانتظار الموافقة |
| `customer1@souq.test` | عميل |

### نقاط نهاية إضافية
| المسار | الصلاحية |
|--------|----------|
| `GET/PATCH /api/v1/site/settings/` | قراءة عامة · تعديل **أدمن فقط** |
| `GET /api/v1/vendors/admin/applications/` · `POST .../<id>/approve/ · /reject/` | أدمن |
| `GET /api/v1/vendors/admin/stats/` | أدمن |
| `GET/POST /api/v1/auth/staff/` · `PATCH/DELETE /staff/<id>/` | صاحب متجر |

---

## الخطوة التالية

حسب [docs/PLAN.md](docs/PLAN.md): **Order service** كامل (يحل محل checkout المؤقت) + **Payment** (Paymob/Fawry/Stripe).
