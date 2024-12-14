from django.shortcuts import render


def index(request):
    return render(request, "../templates/index.html")


def admin(request):
    return render(request, "../templates/admin.html")


def notes(request):
    return render(request, "../templates/notes.html")


def popup(request):
    return render(request, "../templates/popup.html")


def service(request):
    return render(request, "../templates/service.html")


def service_finally(request):
    return render(request, "../templates/serviceFinally.html")
