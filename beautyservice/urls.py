from django.urls import path

from beautyservice import views

app_name = "beautyservice"

urlpatterns = [
    path("", views.index, name="index"),
    path("notes/", views.notes, name="admin"),
    path("popup/", views.popup, name="popup"),
    path("service/", views.service, name="service"),
    path("service_finally/", views.service_finally, name="service_finally"),

    path('api/get_salons/', views.get_salons, name='get_salons'),
    path('api/services/', views.get_services, name='get_services'),
    path('api/masters/', views.get_masters, name='get_masters'),
    path('service/api/get_all_services/', views.get_all_services, name='get_all_services'),
    path('service/api/get_all_masters/', views.get_all_masters, name='get_all_masters'),

]
