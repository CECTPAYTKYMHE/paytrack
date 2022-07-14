from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import calendar
from Calendar.forms import AddCalendarForms, ManualProceed, PaidEventForms
from .models import *
from Calendar.serializers import EventSerializer
from rest_framework import viewsets
from django.views import View
import json
from django.contrib.auth.decorators import login_required


class EventsListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
def eventcontext(request):
    """Контекст для отображения занятий в календаре"""
    events = []
    profile = Profile.objects.get(user=request.user)
    calendar = Calendar.objects.filter(user = profile)
    for event in calendar:
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

@login_required
def home(request):
    json_lessons = eventcontext(request)
    context = {
     'title' : 'Календарь',
     'lessons' : json_lessons,
        }
    return render(request, 'calendar/home.html', context)


class AddCalendar(View):
    """View с добавлнием события календаря, так же в ней создаются ученики если они не существовали
    и создаются события ивентов(уроков)"""
    

    def post(self,request,*args, **kwargs):
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
        calendar = Calendar.objects.create(title=customer[0],
                                time_start = request.POST['start'],
                                time_end = request.POST['end'],
                                price = request.POST['price'],
                                repeat = repeat,
                                telegrambool = telegrambool,
                                user = Profile.objects.get(user = request.user)) #Создаем событие календаря
        
        if repeat:
            addeventfromcalendar(calendar,calendar.time_start, 
                                 calendar.title, 
                                 request.user,
                                 calendar.price) #Создаются повторяющиеся события(уроки) сроком на 1 год
        else:
            Event.objects.create(start=calendar.time_start,
                                 end = calendar.time_start,
                                 title = str(calendar.title).split(' ')[0],
                                 master_event=calendar,
                                 user=request.user,
                                 price_event=calendar.price) #Если не повторяется создается 1 событие

        return HttpResponseRedirect(reverse('calendar:addevent'))
    

    def get(self,request,*args, **kwargs):
        form = AddCalendarForms
        lessons = eventcontext(request)
        students = Customer.objects.filter(user = request.user)
        context = {
        'title' : 'Создание занятий',
        'lessons' : lessons,
        'students': students,
        'form': form,
            }
        return render(request, 'calendar/addevent.html',context)

@login_required
def addeventfromcalendar(calendar, time, title, user, price_event):
    """Создание 52 уроков на год при чек боксе повторяющегося события"""
    title = str(title).split(' ')[0]
    time = datetime.strptime(time,'%Y-%m-%dT%H:%M')
    for i in range(52):
        Event.objects.create(start=time,
                             master_event=calendar,
                             end=time, 
                             title=title,
                             user=user,
                             price_event=price_event)
        time += timedelta(7)


class ShowEvent(View):
    """Показ и изменение события(урока) с чекбоксами о оплате и удаления события"""

    def get(self,request,pk,*args, **kwargs):
        event = Event.objects.get(pk=pk,user=request.user)
        form = PaidEventForms()
        if event.paid:
            form.fields['paid'].widget.attrs['checked'] = ''
        context = {
                'form': form,
                'title' : event.title,
                'event' : event,
            }
        return render(request, 'calendar/event.html',context)
    

    def post(self,request,pk,*args, **kwargs):
        if 'unluck' in request.POST:
            Event.objects.get(pk=pk).delete()
        else:
            if 'paid' in request.POST:
                paid = Event.objects.get(pk=pk)
                paid.paid = True
                paid.save()
            else:
                paid = Event.objects.get(pk=pk)
                paid.paid = False
                paid.save()
        return redirect('calendar:home')

class Proceeds(View):
    def get(self,request,*args, **kwargs):
        """Математика заработка преподавателя"""
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
        context = {
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
        return render(request,'calendar/proceeds.html',context)
        
    def post(self,request,*args, **kwargs):
        form = ManualProceed
        manuallessons = Event.objects.filter(start__range = [self.request.POST['start'],self.request.POST['end']],user=request.user)
        totalmanual = sum([rub.price_event for rub in manuallessons if rub.paid])
        start = datetime.strptime(request.POST['start'],'%Y-%m-%d')
        
        end = datetime.strptime(request.POST['end'],'%Y-%m-%d')
        context = {
            'show': False,
            'form' : form,
            'totalmanual': totalmanual,
            'start': start,
            'end' : end,
        }
        return render(request,'calendar/proceeds.html', context)

    