from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path("", include("apps.general.urls")),
    path("", include("apps.shop.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("admin/", admin.site.urls),
    path("__debug__", include(debug_toolbar.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
