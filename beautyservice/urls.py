from django.urls import path

from beautyservice import views

app_name = "beautyservice"

urlpatterns = [
    path("", views.index, name="index"),
    path("notes/", views.notes, name="admin"),
    path("popup/", views.popup, name="popup"),
    path("service/", views.service, name="service"),
    path("service_finally/", views.service_finally, name="service_finally"),
]