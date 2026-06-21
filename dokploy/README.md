# 🚀 نشر SouqStore على Dokploy

ملف واحد ينشر كل الخدمات (Frontend + Gateway + 3 microservices + قواعد البيانات + Redis + RabbitMQ) على **دومين واحد** عبر Traefik.

## المعمارية في الإنتاج
```
الإنترنت ──(HTTPS)──> Traefik (Dokploy) ──> web (storefront / nginx)
                                              ├─ يخدم تطبيق Vue المبني (dist)
                                              └─ يمرّر /api /ws /media ──> gateway ──> auth · vendor · catalog
```
دومين عام واحد فقط (`${DOMAIN}`) — الباقي شبكة داخلية.

---

## الخطوات

### 1) المتطلبات
- سيرفر عليه **Dokploy** مثبّت (Traefik وشبكة `dokploy-network` جاهزين تلقائياً).
- دومين، واعمل **A record** يشاور على IP السيرفر.

### 2) أنشئ الخدمة في Dokploy
1. New → **Compose**.
2. اربط الريبو (Git) أو ارفع الكود.
3. **Compose Path:** `docker-compose.dokploy.yml`
4. في تبويب **Environment** الصق متغيّرات [.env.dokploy.example](../.env.dokploy.example) وغيّر كل `CHANGE_ME`.
   > توليد مفاتيح: `openssl rand -hex 32`
5. في تبويب **Domains** (أو اعتماداً على labels الجاهزة في الملف): الدومين = `${DOMAIN}`، Port = `80`، فعّل HTTPS (Let's Encrypt).

### 3) Deploy
اضغط **Deploy**. أول مرة بياخد دقائق (بناء صورة الفرونت + الصور). كل خدمة بتعمل `migrate` تلقائياً عند التشغيل.

### 4) عبّي البيانات (مرة واحدة)
من ترمنال السيرفر داخل مجلد المشروع:
```bash
bash dokploy/init.sh
# أو بحجم أكبر:
PRODUCTS=8000 VENDORS=100 bash dokploy/init.sh
```
لو Dokploy مسمّي المشروع باسم معيّن:
```bash
PROJECT=<اسم-المشروع-في-dokploy> bash dokploy/init.sh
```

---

## بعد النشر
- الموقع: `https://${DOMAIN}`
- لوحة الإدارة: `https://${DOMAIN}/admin` — `admin@souq.test` / `Admin12345`
- لوحة المتجر: `https://${DOMAIN}/dashboard` — `vendor1@souq.test` / `Password123`

## تحديثات لاحقة
أي push جديد → **Redeploy** من Dokploy. الترحيلات (migrations) بتتطبّق تلقائياً. البيانات محفوظة في الـ volumes (`*-db-data`, `media-data`) ومش بتتمسح.

## ملاحظات إنتاجية
- `catalog` بيشتغل بـ **daphne** (ASGI) عشان WebSocket؛ `auth`/`vendor` بـ **gunicorn**.
- الصور تُولَّد محلياً داخل `media-data` (لا CDN خارجي).
- لإضافة دومين منفصل للـ API لو حبيت، أضف router label تاني على خدمة `web` أو `gateway`.
- لتغيير ألوان الموقع: من لوحة الأدمن (هو الوحيد المخوّل).
