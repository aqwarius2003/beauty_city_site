from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Master, Salon, Service, Category, Schedule, Note, Client
from datetime import datetime
import json


def auth_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('tel')
        print(f"Phone: {phone}")
        try:
            client = Client.objects.get(phone=phone)
            return JsonResponse({'redirect_url': f'/notes/{client.id}/'})
        except Client.DoesNotExist:
            client = Client.objects.create(phone=phone)
            return JsonResponse({'redirect_url': f'/notes/{client.id}/'})
    return render(request, 'auth.html')


def index(request):
    masters = Master.objects.all()
    salons = Salon.objects.all()
    services = Service.objects.all()

    return render(
        request,
        "index.html",
        context={"masters": masters, "salons": salons, "services": services},
    )


def notes(request, client_id):
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()
    print(current_time)
    client = Client.objects.get(id=client_id)

    upcoming_notes = Note.objects.filter(client_id=client_id,
                                         date__gt=current_date
                                         ) | Note.objects.filter(client_id=client_id,
                                                                 date=current_date,
                                                                 time__gt=current_time
                                                                 )
    past_notes = Note.objects.filter(client_id=client_id,
                                     date__lt=current_date
                                     ) | Note.objects.filter(client_id=client_id,
                                                             date=current_date,
                                                             time__lt=current_time
                                                             )
    
    total_price = sum(note.price for note in upcoming_notes)
    print(total_price)
    context = {
        "upcoming_notes": upcoming_notes,
        "past_notes": past_notes,
        "total_price": total_price,
        "client": client,
        "client_id": client_id
    }

    return render(request, "notes.html", context=context)


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
    unique_salons = Schedule.objects.filter(is_active=True).values('salon__id', 'salon__title').distinct()

    salon_data = [{'id': salon['salon__id'], 'title': salon['salon__title']} for salon in unique_salons]
    print(salon_data)
    return JsonResponse(salon_data, safe=False, json_dumps_params={'ensure_ascii': False})


def get_all_services(request):
    schedules = Schedule.objects.filter(is_active=True)
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
    masters = Master.objects.filter(schedules__isnull=False, schedules__is_active=True).distinct()
    master_data = [{'id': master.id, 'name': master.name, 'profession': master.profession} for master in masters]
    print(master_data)
    return JsonResponse(master_data, safe=False)


def get_services(request):
    salon_id = request.GET.get('salon_id')
    if salon_id:
        schedules = Schedule.objects.filter(salon_id=salon_id, is_active=True).prefetch_related('master__service')
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
        master__service__id=service_id,
        is_active=True

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
                                            date=date, is_active=True)
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
        for key in time_slots:
            time_slots[key].sort(key=lambda x: datetime.strptime(x["time"], '%H:%M'))
        sorted_time_slots = {key: time_slots[key] for key in ["Утро", "День", "Вечер"] if key in time_slots}
        return JsonResponse(sorted_time_slots)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_schedule_for_salon(request):
    master_id = request.GET.get('master_id')
    salon_id = request.GET.get('salon_id')
    date = request.GET.get('date')
    print(f"Master ID: {master_id}, Salon ID: {salon_id}, Date: {date}")
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()

        schedules = Schedule.objects.filter(master_id=master_id,
                                            salon_id=salon_id,
                                            date=date,
                                            is_active=True)
        print(f"Schedules found: {schedules.count()}")
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
        for key in time_slots:
            time_slots[key].sort(key=lambda x: datetime.strptime(x["time"], '%H:%M'))
        sorted_time_slots = {key: time_slots[key] for key in ["Утро", "День", "Вечер"] if key in time_slots}
        print(sorted_time_slots)
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


def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        salon_title = data.get('salon')
        service_title = data.get('service')
        master_name = data.get('master')
        time = data.get('time')
        date = data.get('date')
        name = data.get('fname')
        phone = data.get('tel')
        question = data.get('contactsTextarea', '')
        print(f"Salon: {salon_title}, Service: {service_title}, Master: {master_name}, Time: {time}, Date: {date}, Name: {name}, Phone: {phone}")
        if not (salon_title and service_title and master_name and time and date and name and phone):
            return JsonResponse({'success': False, 'error': 'Все обязательные поля должны быть заполнены.'}, status=400)

        salon = Salon.objects.get(title=salon_title)
        service = Service.objects.get(name=service_title)
        master = Master.objects.get(name=master_name)
        schedule = Schedule.objects.get(salon=salon, master=master, date=date, time=time)
        client, created = Client.objects.get_or_create(phone=phone)
        if created:
            client.name = name
            client.save()
        else:
            client.name = name
            client.save()
            
        note = Note.objects.create(
            salon=salon,
            client=client,
            master=master,
            service=service,
            price=service.price,
            date=schedule.date,
            time=schedule.time
        )
        schedule.is_active = False
        schedule.save()
        return JsonResponse({'success': True, 'message': 'Запись успешно создана!', 'note_id': note.id})


def get_master_for_service(request):
    service_id = request.GET.get('service_id')

    try:
        master_data = []
        master = Master.objects.filter(service=service_id, schedules__is_active=True).distinct()
        for m in master:
            master_data.append({'id': m.id, 'name': m.name, 'profession': m.profession})
        return JsonResponse(master_data, safe=False)
    except Master.DoesNotExist:
        return JsonResponse({'error': 'Master not found'}, status=404)

def get_salon_for_service(request):
    service_id = request.GET.get('service_id')

    try:
        master = Master.objects.filter(service=service_id, schedules__is_active=True).distinct()

        salon_data = []
        salon = Salon.objects.filter(masters__service=service_id, masters__schedules__is_active=True, masters__in=master).distinct()
        for s in salon:
            salon_data.append({'id': s.id, 'title': s.title})
        return JsonResponse(salon_data, safe=False)
    except Salon.DoesNotExist:
        return JsonResponse({'error': 'Salon not found'}, status=404)


def get_salons_for_date(request):
    date = request.GET.get('date')
    master = request.GET.get('master')

    master = Master.objects.get(id=master)
    try:
        salon_data = []
        salon = Salon.objects.filter(schedules__date=date, schedules__is_active=True, schedules__master=master).distinct()
        for s in salon:
            salon_data.append({'id': s.id, 'title': s.title})
        return JsonResponse(salon_data, safe=False)
    except Salon.DoesNotExist:
        return JsonResponse({'error': 'Salon not found'}, status=404)