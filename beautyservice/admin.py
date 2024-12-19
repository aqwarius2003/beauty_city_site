from django.contrib import admin

from .models import Salon, Master, Service, Category, Schedule, Note, Client


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


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("salon", "master", "date", "time")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "salon", "created_at")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
