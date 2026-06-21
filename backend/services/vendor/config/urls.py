from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.stores.admin_views import SiteSettingsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/vendors/", include("apps.stores.urls")),
    path("api/v1/site/settings/", SiteSettingsView.as_view(), name="site-settings"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
