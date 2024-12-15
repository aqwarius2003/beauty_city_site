from django.shortcuts import render

from .models import Master, Salon, Service


def index(request):
    masters = Master.objects.all()
    salons = Salon.objects.all()
    services = Service.objects.all()

    return render(request, 'index.html', context={
        'masters': masters,
        'salons': salons,
        'services': services
    })


def notes(request):
    return render(request, "../templates/notes.html")


def popup(request):
    return render(request, "../templates/popup.html")


def service(request):
    return render(request, "../templates/service.html")


def service_finally(request):
    return render(request, "../templates/serviceFinally.html")
