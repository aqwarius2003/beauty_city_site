from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("main/", include("users.urls", namespace="users")),
    path("admin/", admin.site.urls),
]
