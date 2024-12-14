from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", views.admin, name="admin"),
    path("notes/", views.notes, name="admin"),
]
