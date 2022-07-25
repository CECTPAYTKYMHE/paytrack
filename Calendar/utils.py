import calendar

from django.shortcuts import redirect
from Calendar.forms import ManualProceed
from .models import *
from datetime import date, datetime, timedelta
import json 


def create_event_context(request) -> json:
    """Создание контекста для отображения занятий в календаре"""
    events = []
    profile = Profile.objects.get(user=request.user)
    customer_calendar = Calendar.objects.filter(user = profile)
    for event in customer_calendar:
        events.append(Event.objects.filter(master_event = event))
    lessons = []
    for event in events:
        for lesson in event:
            if lesson.__dict__['paid']:
                paid = '#0fd108'
            else:
                paid = '#6c786c'
            lessons.append(
                {
                    'title' : f"{str(lesson.__dict__['title'])}",
                    'start' : datetime.strftime(lesson.__dict__['start'],'%Y-%m-%d %H%M'),
                    'end': datetime.strftime(lesson.__dict__['end'],'%Y-%m-%d %H%M'),
                    'url': '/home/event/' + str(lesson.__dict__['id']),
                    'borderColor': paid,
                    'backgroundColor' : paid,
                }
            )
    json_lessons = json.dumps(lessons, indent = 4)  
    return json_lessons


def add_event_from_calendar(customer_calendar, time_start, time_end, title, user, price_event):
    """Создание 52 уроков на год при чек боксе повторяющегося события"""
    title = str(title).split(' ')[0]
    time_start = datetime.strptime(time_start,'%Y-%m-%dT%H:%M')
    time_end = datetime.strptime(time_end,'%Y-%m-%dT%H:%M')
    objs = []
    for i in range(52):
        objs.append(Event(start=time_start,
                            master_event=customer_calendar,
                            end=time_end, 
                            title=title,
                            user=user,
                            price_event=price_event))
        time_start += timedelta(7)
        time_end += timedelta(7)
    Event.objects.bulk_create(objs)


def add_calendar_and_event(request):
    """Создание главного события и 52 ивентов при повторяющихся событиях"""
    if 'repeat' in request.POST:
        repeat = True
    else:
        repeat = False
    if 'telegramm' in request.POST:
        telegrambool = True
    else:
        telegrambool = False
        
    customer = Customer.objects.get_or_create(name = request.POST['title'],
                                                user_id=request.user.id) #Создание ученика если его не существует
    
    customer_calendar = Calendar.objects.create(title=customer[0],
                                time_start = request.POST['start'],
                                time_end = request.POST['end'],
                                price = request.POST['price'],
                                repeat = repeat,
                                telegrambool = telegrambool,
                                user = Profile.objects.get(user = request.user)) #Создаем событие календаря
        
    if repeat:
        add_event_from_calendar(customer_calendar,
                                customer_calendar.time_start, 
                                customer_calendar.time_end,
                                customer_calendar.title, 
                                request.user,
                                customer_calendar.price) #Создаются повторяющиеся события(уроки) сроком на 1 год
    else:
        Event.objects.create(start=customer_calendar.time_start,
                            end = customer_calendar.time_end,
                            title = str(customer_calendar.title).split(' ')[0],
                            master_event=customer_calendar,
                            user=request.user,
                            price_event=customer_calendar.price) #Если не повторяется создается 1 событие
        

def event_edit(request, pk):  
    """Удаление цепочки неоплаченных уроков, отмена занятий и чек бокс оплаты, заметки о ученике""" 
    master = Event.objects.get(pk=pk)
    if 'unluck' in request.POST:
        Event.objects.get(pk=pk).delete()
        return redirect('calendar:home')
    if 'delcalendar' in request.POST:
        master_event = Calendar.objects.get(pk=master.master_event_id)
        Event.objects.filter(master_event=master_event, paid = False).delete()
        return redirect('calendar:home')
    else:
        if 'paid' in request.POST:
            paid = Event.objects.get(pk=pk)
            paid.paid = True
            paid.save()
        else:
            paid = Event.objects.get(pk=pk)
            paid.paid = False
            paid.save()
    student = Customer.objects.get(name=master.title, user=request.user)
    student.description = request.POST['description']
    student.save()


def calculate_proceeds_for_get(request) -> dict:
    """Калькуляция заработка за месяц и неделю"""
    theday = date.today()
    weekday = theday.isoweekday()
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    first_date = date(year, month, 1)
    last_date = date(year, month, number_of_days)
    last_date = last_date + timedelta(days=1)
    start = theday - timedelta(days=weekday-1)
    dates_week = [start + timedelta(days=d) for d in range(8)]
    weeklessons = Event.objects.filter(start__range = [dates_week[0],dates_week[7]],user=request.user)
    monthlessons = Event.objects.filter(start__range = [first_date,last_date],user=request.user)
    unpaidweek = len([day for day in weeklessons if day.paid == False])
    cash_week_earn = sum([allrub.price_event for allrub in weeklessons if allrub.paid])
    cash_week_unearn = sum([allrub.price_event for allrub in weeklessons if not allrub.paid])
    all_earn_week = cash_week_earn + cash_week_unearn
    unpaidmonth = len([day for day in monthlessons if day.paid == False])
    cash_month_earn = sum([allrub.price_event for allrub in monthlessons if allrub.paid])
    cash_month_unearn = sum([allrub.price_event for allrub in monthlessons if not allrub.paid])
    all_earn_month = cash_month_earn + cash_month_unearn
    form = ManualProceed
    return {
        'show': True,
        'unpaidweek' : unpaidweek,
        'weeklessons' : len(weeklessons),
        'cash_week_earn' : cash_week_earn,
        'cash_week_unearn' : cash_week_unearn,
        'all_earn_week' : all_earn_week,
        'monthlessons': len(monthlessons),
        'unpaidmonth': unpaidmonth,
        'cash_month_earn': cash_month_earn,
        'cash_month_unearn': cash_month_unearn,
        'all_earn_month': all_earn_month,
        'form' : form,    
    }


def calculate_proceeds_for_post(request):
    """Калькуляция заработка по выбору дат пользователем"""
    form = ManualProceed
    manuallessons = Event.objects.filter(start__range = [request.POST['start'],request.POST['end']],user=request.user)
    totalmanual = sum([rub.price_event for rub in manuallessons if rub.paid])
    start = datetime.strptime(request.POST['start'],'%Y-%m-%d')
        
    end = datetime.strptime(request.POST['end'],'%Y-%m-%d')
    return {
            'show': False,
            'form' : form,
            'totalmanual': totalmanual,
            'start': start,
            'end' : end,
        }