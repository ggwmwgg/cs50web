from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

handler404 = "network.views.not_found"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("network.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
