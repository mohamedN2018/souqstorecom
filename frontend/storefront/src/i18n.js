import { createI18n } from "vue-i18n";

const messages = {
  ar: {
    brand: "سوق ستور",
    nav: { home: "الرئيسية", products: "المنتجات", vendors: "المتاجر", cart: "السلة" },
    home: {
      hero_title: "كل اللي محتاجه في سوق واحد",
      hero_sub: "آلاف المنتجات من مئات المتاجر الموثوقة — بأفضل الأسعار وتوصيل سريع.",
      shop_now: "تسوّق الآن",
      featured: "منتجات مميزة",
      categories: "تسوّق حسب الفئة",
      top_vendors: "متاجر مميزة",
      flash: "عروض اليوم تنتهي خلال",
    },
    product: { add_to_cart: "أضف للسلة", buy_now: "اشترِ الآن", reviews: "التقييمات", sold: "تم بيع", off: "خصم" },
    common: { currency: "ج.م", search: "ابحث عن منتج...", filters: "الفلاتر", price: "السعر", rating: "التقييم", all: "الكل", loading: "جاري التحميل...", empty: "لا توجد نتائج" },
    theme: { customize: "خصّص الألوان", primary: "الأساسي", accent: "المميِّز", reset: "إعادة ضبط" },
  },
  en: {
    brand: "SouqStore",
    nav: { home: "Home", products: "Products", vendors: "Stores", cart: "Cart" },
    home: {
      hero_title: "Everything you need in one souq",
      hero_sub: "Thousands of products from hundreds of trusted stores.",
      shop_now: "Shop now",
      featured: "Featured products",
      categories: "Shop by category",
      top_vendors: "Top stores",
      flash: "Today's deals end in",
    },
    product: { add_to_cart: "Add to cart", buy_now: "Buy now", reviews: "Reviews", sold: "Sold", off: "OFF" },
    common: { currency: "EGP", search: "Search products...", filters: "Filters", price: "Price", rating: "Rating", all: "All", loading: "Loading...", empty: "No results" },
    theme: { customize: "Customize colors", primary: "Primary", accent: "Accent", reset: "Reset" },
  },
};

export const i18n = createI18n({
  legacy: false,
  locale: "ar",
  fallbackLocale: "en",
  messages,
});

export function setLocale(locale) {
  i18n.global.locale.value = locale;
  document.documentElement.lang = locale;
  document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
}
