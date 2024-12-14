from django.shortcuts import render


def index(request):
    return render(request, "../templates/index.html")


def admin(request):
    return render(request, "../templates/admin.html")


def notes(request):
    return render(request, "../templates/notes.html")
