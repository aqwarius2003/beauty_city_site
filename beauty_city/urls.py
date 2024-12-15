from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import settings

urlpatterns = [
    path("", include("beautyservice.urls", namespace="beautyservice")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
