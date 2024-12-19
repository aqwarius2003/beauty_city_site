from django.http import JsonResponse
from django.shortcuts import render

from .models import Master, Salon, Service, Category, Schedule, Note
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


def notes(request, client_id=1):
    notes = Note.objects \
        .filter(client_id=client_id) \
        .select_related('service', 'master', 'salon')
    total_price = 0
    for note in notes:
        total_price += note.price

    context = {
        'notes': notes,
        'total_price': total_price
    }

    return render(request, "../templates/notes.html", context=context)


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
    salon = request.GET.get('salon')
    service = request.GET.get('service')
    master = request.GET.get('master')
    date = request.GET.get('date')
    time = request.GET.get('time')

    salon = Salon.objects.get(id=salon)
    service = Service.objects.get(id=service)
    master = Master.objects.get(id=master)

    print(salon, service, master, date, time, salon.address)
    return render(
        request,
        context={
            "salon": salon,
            "service": service,
            "master": master,
            "date": date,
            "time": time
        },
        template_name="../templates/serviceFinally.html"
    )


def get_salons(request):
    unique_salons = Schedule.objects.values('salon__id', 'salon__title').distinct()

    salon_data = [{'id': salon['salon__id'], 'title': salon['salon__title']} for salon in unique_salons]
    print(salon_data)
    return JsonResponse(salon_data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_all_services(request):
    schedules = Schedule.objects.all()
    service_list = []
    unique_service_ids = set()

    for schedule in schedules:
        master = schedule.master
        services = master.service.all()
        for service in services:
            if service.id not in unique_service_ids:
                unique_service_ids.add(service.id)
                service_list.append(
                    {
                        'id': service.id,
                        'name': service.name,
                        'price': service.price,
                        'category': service.category.name,
                    }
                )

    print(service_list)
    return JsonResponse(service_list, safe=False)


def get_all_masters(request):
    masters = Master.objects.filter(schedules__isnull=False).distinct()
    master_data = [{'id': master.id, 'name': master.name, 'profession': master.profession} for master in masters]
    print(master_data)
    return JsonResponse(master_data, safe=False)


def get_services(request):
    salon_id = request.GET.get('salon_id')
    if salon_id:
        schedules = Schedule.objects.filter(salon_id=salon_id).prefetch_related('master__service')
        unique_services = {}

        for schedule in schedules:
            master = schedule.master
            services = master.service.all()

            for service in services:
                # if service.id not in unique_services:
                unique_services[service.id] = {
                    'id': service.id,
                    'name': service.name,
                    'price': service.price,
                    'category': service.category.name,
                }

        service_list = list(unique_services.values())
        print(service_list)
        return JsonResponse(service_list, safe=False)

    return JsonResponse({'error': 'Salon ID is required'}, status=400)


def get_masters(request):
    service_id = request.GET.get('service_id')
    salon_id = request.GET.get('salon_id')

    if not service_id or not salon_id:
        return JsonResponse({'error': 'Service ID and Salon ID are required'}, status=400)

    schedules = Schedule.objects.filter(
        salon_id=salon_id,
        master__service__id=service_id
    ).prefetch_related('master').distinct()

    masters = {schedule.master.id: schedule.master for schedule in schedules}

    master_data = [
        {'id': master.id, 'name': master.name, 'profession': master.profession}
        for master in masters.values()
    ]
    print(master_data)
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
        date = datetime.strptime(date, '%Y-%m-%d').date()

        schedules = Schedule.objects.filter(master_id=master_id,
                                            date=date)
        print(schedules)
        time_slots = {}
        for schedule in schedules:
            if schedule.is_active:
                time_slot = {
                    "time": schedule.time.strftime('%H:%M'),
                    "salon_id": schedule.salon_id
                }
                time_of_day = get_time_of_day(schedule.time)
                if time_of_day not in time_slots:
                    time_slots[time_of_day] = []
                time_slots[time_of_day].append(time_slot)
        print(time_slots)
        return JsonResponse(time_slots)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_schedule_for_salon(request):
    master_id = request.GET.get('master_id')
    salon_id = request.GET.get('salon_id')
    date = request.GET.get('date')

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        schedules = Schedule.objects.filter(master_id=master_id,
                                            salon_id=salon_id,
                                            date=date)
        time_slots = {}
        for schedule in schedules:
            if schedule.is_active:
                time_slot = {
                    "time": schedule.time.strftime('%H:%M'),
                    "salon_id": schedule.salon_id
                }
                time_of_day = get_time_of_day(schedule.time)
                if time_of_day not in time_slots:
                    time_slots[time_of_day] = []
                time_slots[time_of_day].append(time_slot)

        sorted_time_slots = {key: time_slots[key] for key in ["Утро", "День", "Вечер"] if key in time_slots}
        return JsonResponse(sorted_time_slots)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_time_of_day(time):
    if 6 <= time.hour < 12:
        return 'Утро'
    elif 12 <= time.hour < 18:
        return 'День'
    elif 18 <= time.hour < 22:
        return 'Вечер'
    else:
        return 'Ночь'
