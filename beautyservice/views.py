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
    all_type_category = [(i.name, i.services.all()) for i in cat]
    return render(
        request=request,
        context={
            "salons": salons,
            "masters": masters,
            "all_type_category": all_type_category,
        },
        template_name="../templates/service.html",
    )


def service_finally(request):
    return render(request, "../templates/serviceFinally.html")
