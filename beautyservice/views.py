from django.shortcuts import render

from .models import Master, Salon, Service, Category


def index(request):
    masters = Master.objects.all()
    salons = Salon.objects.all()
    services = Service.objects.all()

    return render(
        request,
        "index.html",
        context={"masters": masters, "salons": salons, "services": services},
    )


def notes(request):
    return render(request, "../templates/notes.html")


def popup(request):
    return render(request, "../templates/popup.html")


def service(request):
    masters = Master.objects.all()
    salons = Salon.objects.all()

    cat = Category.objects.all()
    info_about_service = {}
    for i in cat:
        name_services = i.services.all()
        services_list = [(j.name, j.price) for j in name_services]
        info_about_service[i.name] = services_list

    return render(
        request=request,
        context={
            "salons": salons,
            "masters": masters,
            "info_about_service": info_about_service,
        },
        template_name="../templates/service.html",
    )


def service_finally(request):
    return render(request, "../templates/serviceFinally.html")
