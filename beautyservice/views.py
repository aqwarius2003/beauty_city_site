from django.http import JsonResponse
from django.shortcuts import render

from .models import Master, Salon, Service, Category, Schedule
from .models import Schedule
from datetime import datetime


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
    schedule = Schedule.objects.filter(is_active=True)

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
            "schedule": schedule
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


def get_salons_for_masters_and_services(request):
    master_id = request.GET.get('master_id')
    service_id = request.GET.get('service_id')

    if not master_id or not service_id:
        return JsonResponse({'error': 'Master ID and Service ID are required'}, status=400)

    try:
        master = Master.objects.get(id=master_id)
    except Master.DoesNotExist:
        return JsonResponse({'error': 'Master not found'}, status=404)

    salons = Salon.objects.filter(masters=master)

    salons_with_service = salons.filter(masters__service__id=service_id).distinct()

    salon_data = [{'id': salon.id, 'title': salon.title} for salon in salons_with_service]

    return JsonResponse(salon_data, safe=False)


def get_schedule(request):
    master_id = request.GET.get('master_id')
    date = request.GET.get('date')

    try:
        # Преобразуем строку даты в объект datetime
        date = datetime.strptime(date, '%Y-%m-%d').date()

        # Получаем все расписания для выбранного мастера и даты
        schedules = Schedule.objects.filter(master_id=master_id, date=date)
        print(schedules)
        # Разбиваем расписание по времени
        time_slots = {}
        for schedule in schedules:
            if schedule.is_active:
                time_slot = {
                    "time": schedule.time.strftime('%H:%M'),
                    "salon_id": schedule.salon_id  # Используем salon_id из модели Schedule
                }
                time_of_day = get_time_of_day(schedule.time)
                if time_of_day not in time_slots:
                    time_slots[time_of_day] = []
                time_slots[time_of_day].append(time_slot)
        return JsonResponse(time_slots)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_time_of_day(time):
    """Определяем часть дня: утро, день, вечер."""
    if 6 <= time.hour < 12:
        return 'Утро'
    elif 12 <= time.hour < 18:
        return 'День'
    elif 18 <= time.hour < 22:
        return 'Вечер'
    else:
        return 'Ночь'
