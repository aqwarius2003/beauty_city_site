from django.contrib import admin

from .models import Salon, Master, Service, Category


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ("title", "address", "image")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("name", "profession")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
