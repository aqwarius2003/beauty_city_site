from django.http import JsonResponse
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
    categories = Category.objects.all()

    info_about_service: dict[str, list[tuple[str, int]]] = {}
    for category in categories:
        services = category.services.all()
        services_list = [{"name": service.name, "price": service.price, "id": service.id} for service in services]
        info_about_service[category.name] = services_list

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


def get_salons(request):
    salons = Salon.objects.all()
    salon_data = [{'id': salon.pk, 'title': salon.title} for salon in salons]
    return JsonResponse(salon_data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_all_services(request):
    services = Service.objects.all()
    service_list = [
        {
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'category': service.category.name,
        }
        for service in services
    ]

    return JsonResponse(service_list, safe=False)


def get_all_masters(request):
    masters = Master.objects.all()
    master_data = [{'id': master.id, 'name': master.name, 'profession': master.profession} for master in masters]
    return JsonResponse(master_data, safe=False)


def get_services(request):
    salon_id = request.GET.get('salon_id')
    if salon_id:
        salon = Salon.objects.get(id=salon_id)

        masters_in_salon = Master.objects.filter(salon=salon)

        services = Service.objects.filter(masters__in=masters_in_salon).distinct()
        service_list = [
            {
                'id': service.id,
                'name': service.name,
                'price': service.price,
                'category': service.category.name,
            }
            for service in services
        ]
        print(service_list)
        return JsonResponse(service_list, safe=False)

    return JsonResponse({'error': 'Salon ID is required'}, status=400)


def get_masters(request):
    service_id = request.GET.get('service_id')
    salon_id = request.GET.get('salon_id')
    if not service_id or not salon_id:
        return JsonResponse({'error': 'Service ID and Salon ID are required'}, status=400)

    masters = Master.objects.filter(
        service__id=service_id,
        salon__id=salon_id
    ).distinct()

    master_data = [
        {'id': master.id, 'name': master.name, 'profession': master.profession}
        for master in masters
    ]
    return JsonResponse(master_data, safe=False)


def get_services_for_masters(request):
    master_id = request.GET.get('master_id')

    if not master_id:
        return JsonResponse({'error': 'Master ID is required'}, status=400)

    services = Service.objects.filter(masters__id=master_id).distinct()
    service_list = [
        {
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'category': service.category.name,
        }
        for service in services
    ]

    return JsonResponse(service_list, safe=False)