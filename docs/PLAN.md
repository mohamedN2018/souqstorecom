# 🛒 SouqStore — خطة بناء منصة Marketplace متعددة البائعين

> منصة سوق إلكتروني (Marketplace) — موقع واحد، بائعين كُثُر، سلة موحّدة.
> معمارية Microservices · Django (Backend) · Vue 3 (Frontend) · Docker · تخصيص كامل من لوحة التحكم.

---

## 1. القرارات المعتمدة

| القرار | الاختيار |
|--------|----------|
| نموذج المتاجر | **Marketplace** (سوق واحد · بائعون متعددون · دومين واحد) |
| البنية | **Microservices** من البداية + API Gateway + Message Broker |
| الدفع | **Paymob · Fawry · InstaPay · COD** (عربي) + **Stripe · PayPal** (دولي) |
| العملة واللغة | Multi-currency · RTL (عربي) + LTR (إنجليزي) |
| التخصيص | **Full Custom** للألوان/الثيم من لوحة التحكم بدون لمس الكود |

---

## 2. المعمارية العامة (Microservices Map)

```
                                  ┌────────────────────────┐
                                  │      Vue 3 SPA/SSR      │
                                  │  Tailwind · GSAP · i18n │
                                  └───────────┬────────────┘
                                              │ HTTPS / REST + WS
                                  ┌───────────▼────────────┐
                                  │      API GATEWAY        │
                                  │  (Kong / Nginx + Auth)  │
                                  │  Rate-limit · Routing   │
                                  └───────────┬────────────┘
        ┌──────────────┬──────────────┬───────┴──────┬──────────────┬───────────────┐
        ▼              ▼              ▼              ▼              ▼               ▼
  ┌──────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐  ┌────────────┐  ┌────────────┐
  │  Auth /  │  │  Vendor / │  │  Catalog  │  │  Cart    │  │   Order    │  │  Payment   │
  │ Identity │  │   Store   │  │ +Search   │  │          │  │            │  │            │
  └────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────┬─────┘  └─────┬──────┘  └─────┬──────┘
       │ DB           │ DB          │ DB           │ Redis        │ DB            │ DB
  ┌────────┐  ┌───────────┐  ┌──────────────┐                ┌──────────┐  ┌────────────┐
  │Promotion│  │ Shipping  │  │ Notification │   ┌──────────┐ │ Reviews  │  │  Media /   │
  │ /Events │  │           │  │ Email/SMS/WS │   │Analytics │ │ Ratings  │  │   CDN      │
  └────┬────┘  └─────┬─────┘  └──────┬───────┘   └──────────┘ └──────────┘  └────────────┘
       │             │               │
       └─────────────┴───────────────┴──────────►  RabbitMQ / Kafka (Event Bus)
                                                    Redis (Cache/Sessions)
                                                    Elasticsearch / Meilisearch (Search)
                                                    PostgreSQL × N (Database-per-Service)
                                                    MinIO / S3 (Media)
```

**مبدأ أساسي:** كل خدمة عندها قاعدة بياناتها الخاصة (Database-per-Service) → لو خدمة وقعت، الباقي يفضل شغّال. التواصل غير المتزامن عبر Event Bus لمنع الانهيار المتسلسل.

---

## 3. تقسيم الخدمات (Services)

| # | الخدمة | المسؤولية | قاعدة البيانات |
|---|--------|-----------|----------------|
| 1 | **API Gateway** | توجيه · مصادقة الطلبات · Rate-limiting · CORS | — |
| 2 | **Auth / Identity** | تسجيل · JWT · أدوار (Customer/Vendor/Admin) · OAuth | PostgreSQL |
| 3 | **Vendor / Store** | ملفات البائعين · إعدادات المتجر · **الثيم والألوان** · التحقق | PostgreSQL |
| 4 | **Catalog** | منتجات · فئات · خصائص · variants · بحث | PostgreSQL + Meilisearch |
| 5 | **Inventory** | المخزون · الحجز عند الطلب | PostgreSQL |
| 6 | **Cart** | السلة (متعددة البائعين) · حفظ مؤقت | Redis + PostgreSQL |
| 7 | **Order** | الطلبات · التقسيم حسب البائع · الحالة · saga | PostgreSQL |
| 8 | **Payment** | Paymob · Fawry · Stripe · PayPal · COD · Webhooks · تقسيم العمولة | PostgreSQL |
| 9 | **Shipping** | شركات الشحن · حساب التكلفة · التتبّع | PostgreSQL |
| 10 | **Promotion / Events** | كوبونات · عروض · فلاش سيل · **events موسمية** · العدّاد التنازلي | PostgreSQL + Redis |
| 11 | **Review / Rating** | تقييمات · مراجعات · رد البائع | PostgreSQL |
| 12 | **Notification** | إيميل · SMS · Push · WebSocket (إشعارات لحظية) | PostgreSQL |
| 13 | **Media** | رفع الصور · معالجة · CDN | MinIO/S3 |
| 14 | **Analytics** | إحصائيات البائع · المبيعات · لوحات التحكم | ClickHouse/PostgreSQL |

---

## 4. Backend Stack & Best Practices (Django)

- **Django 5 + Django REST Framework (DRF)** لكل خدمة (كل خدمة Django مستقلة).
- **هيكلة المشروع:** Domain-Driven — كل خدمة فيها `apps/` معزولة (models, services, selectors, api).
  - فصل المنطق: `services.py` (write) و `selectors.py` (read) بدل ما يتحط كله في الـ views/serializers.
- **المصادقة:** JWT (SimpleJWT) + Refresh tokens، التحقق المركزي في الـ Gateway.
- **التواصل بين الخدمات:**
  - متزامن: REST عبر الـ Gateway (للقراءة الفورية فقط).
  - غير متزامن: **Celery + RabbitMQ/Kafka** للأحداث (order.created → notification, inventory, payment).
- **النمط:** Saga Pattern للطلبات الموزّعة (إنشاء طلب → دفع → خصم مخزون → شحن) مع تعويض (compensation) عند الفشل.
- **الأدوات:** `drf-spectacular` (OpenAPI docs) · `django-environ` (config) · `pytest-django` (اختبارات) · `ruff` + `black` (linting).
- **Caching:** Redis لنتائج القراءة المتكررة (catalog, store theme).

---

## 5. Frontend Stack (Vue 3)

- **Vue 3 (Composition API) + Vite** — أو **Nuxt 3** لو محتاجين SSR/SEO (موصى به للـ Marketplace عشان السيو).
- **Tailwind CSS** للتصميم + نظام **CSS Variables** ديناميكي للألوان (يتحقن من إعدادات المتجر).
- **GSAP** للأنميشن (hero, transitions, scroll reveal, flash-sale counters).
- **Pinia** لإدارة الحالة (cart, auth, theme).
- **Vue-i18n** للعربي/الإنجليزي + تبديل RTL/LTR تلقائي.
- **التجاوب (Responsive):** Mobile-first بالكامل عبر Tailwind breakpoints.
- واجهات منفصلة: (أ) واجهة المتسوّق · (ب) لوحة البائع · (ج) لوحة الأدمن.

---

## 6. نظام التخصيص الكامل للألوان والثيم (Full Custom)

الهدف: التحكم في كل شيء من **لوحة التحكم** بدون رجوع للكود.

1. **Theme Service** (داخل Vendor/Store) يخزّن: ألوان (primary/secondary/accent)، خطوط، شعار، تخطيط الهيدر/الفوتر، بانرات.
2. الفرونت يقرأ الإعدادات → يحقنها كـ **CSS Custom Properties** (`--color-primary`, ...) على الـ `:root`.
3. Tailwind يستخدم `var(--color-primary)` بدل ألوان ثابتة → أي تغيير ينعكس فوراً.
4. لوحة تحكم بصرية (Theme Editor) فيها معاينة حيّة (Live Preview) للألوان والتخطيط.
5. يدعم: ثيم عام للسوق + ثيم خاص لكل بائع (واجهة متجره).

---

## 7. نظام العروض والـ Events

- **أنواع العروض:** نسبة خصم · مبلغ ثابت · اشترِ X واحصل Y · شحن مجاني · كوبونات.
- **Flash Sales / Events موسمية:** بوقت بداية ونهاية + **عدّاد تنازلي** (GSAP) + Banner ديناميكي.
- **القواعد:** حد أدنى للسلة · فئات محددة · بائع محدد · حد للاستخدام.
- جدولة عبر Celery Beat (تفعيل/إيقاف العروض تلقائياً).

---

## 8. Docker & البنية التحتية (المرونة)

- **كل خدمة = Container مستقل** → عزل كامل للأعطال.
- `docker-compose.yml` للتطوير · إعداد جاهز للـ **Kubernetes** للإنتاج.
- **Health checks** + `restart: unless-stopped` لكل خدمة → الخدمة الواقعة تقوم لوحدها.
- **Circuit Breaker** (مثل مكتبة في الـ Gateway) → لو خدمة وقعت، الباقي ميتأثرش.
- مكوّنات مشتركة: PostgreSQL (×N) · Redis · RabbitMQ · Meilisearch · MinIO · Nginx.
- **Observability:** Prometheus + Grafana (مراقبة) · Loki/ELK (logs مركزية) · Sentry (أخطاء).

---

## 9. الأمان

- JWT + HTTPS إجباري · تشفير كلمات السر (Argon2).
- التحقق من الصلاحيات على مستوى كل خدمة (RBAC).
- Rate-limiting + WAF على الـ Gateway.
- Webhooks موقّعة (Paymob/Stripe signature verification).
- عزل بيانات البائعين (vendor scoping) في كل استعلام.

---

## 10. خارطة الطريق (Phased Roadmap)

### المرحلة 0 — التأسيس (Infra Foundation)
- إعداد monorepo · Docker Compose · Gateway · PostgreSQL/Redis/RabbitMQ · CI/CD.
- هيكل Django مشترك (cookiecutter) + هيكل Vue.

### المرحلة 1 — النواة (MVP Core)
- Auth Service (تسجيل · أدوار · JWT).
- Vendor/Store Service (تسجيل بائع · ملف متجر).
- Catalog Service (منتجات · فئات · بحث).
- واجهة متسوّق أساسية (عرض منتجات · صفحة منتج).

### المرحلة 2 — الشراء
- Cart + Order Service (سلة متعددة البائعين · تقسيم الطلب).
- Payment Service (Paymob + COD أولاً، ثم Stripe).
- Inventory + Shipping.

### المرحلة 3 — التجربة والنمو
- Promotion/Events (عروض · flash sales · كوبونات).
- Reviews + Notifications (WebSocket).
- **Theme Editor** (التخصيص الكامل للألوان).
- لوحة تحكم البائع + الأدمن (Analytics).

### المرحلة 4 — التوسّع
- Search متقدم (Meilisearch/Elasticsearch) · توصيات.
- Multi-currency · Multi-language كامل.
- Kubernetes · Auto-scaling · Observability كامل.

---

## 11. هيكل المجلدات المقترح (Monorepo)

```
souqstorecom/
├── docs/
├── gateway/                  # API Gateway (Kong/Nginx config)
├── services/
│   ├── auth/                 # Django service
│   ├── vendor/
│   ├── catalog/
│   ├── cart/
│   ├── order/
│   ├── payment/
│   ├── inventory/
│   ├── shipping/
│   ├── promotion/
│   ├── review/
│   ├── notification/
│   └── media/
├── frontend/
│   ├── storefront/           # Vue/Nuxt — واجهة المتسوّق
│   ├── vendor-dashboard/     # لوحة البائع
│   └── admin-panel/          # لوحة الأدمن
├── shared/                   # مكتبات مشتركة (events schema, utils)
├── infra/
│   ├── docker-compose.yml
│   ├── k8s/
│   └── monitoring/
└── README.md
```

---

## 12. الخطوة الجاية

أبدأ بـ **المرحلة 0** (التأسيس): هيكل المجلدات + Docker Compose + Gateway + أول خدمة (Auth).
هل أبدأ تنفيذ المرحلة 0 الآن؟
