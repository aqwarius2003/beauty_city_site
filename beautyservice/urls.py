from django.urls import path

from beautyservice import views

app_name = "beautyservice"

urlpatterns = [
    path("", views.index, name="index"),
    path('auth/', views.auth_view, name='auth'),
    path('notes/<int:client_id>/', views.notes, name='notes'),
    path("popup/", views.popup, name="popup"),
    path("service/", views.service, name="service"),
    path("service_finally/", views.service_finally, name="service_finally"),

    path('api/get_salons/', views.get_salons, name='get_salons'),
    path('api/services/', views.get_services, name='get_services'),
    path('api/masters/', views.get_masters, name='get_masters'),
    path('service/api/get_all_services/', views.get_all_services, name='get_all_services'),
    path('service/api/get_all_masters/', views.get_all_masters, name='get_all_masters'),
    path('api/get_services_for_masters/',
         views.get_services_for_masters,
         name='get_services_for_masters'
         ),
    path('api/get_salons_for_masters_and_services/',
         views.get_salons_for_masters_and_services,
         name='get_salons_for_masters_and_services'
         ),

    path('api/get_schedule/', views.get_schedule, name='get_schedule'),
    path('api/get_schedule_for_salon/', views.get_schedule_for_salon, name='get_schedule_for_salon'),
    path('create_order/', views.create_order, name='create_order'),
    path('service/api/get_master_for_service/', views.get_master_for_service, name='get_master_for_service'),
    path('service/api/get_salon_for_service/', views.get_salon_for_service, name='get_salon_for_service'),
    path('api/get_salons_for_date/', views.get_salons_for_date, name='get_salons_for_date'),
]

