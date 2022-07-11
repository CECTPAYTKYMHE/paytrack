from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import requests

from Calendar.forms import AddCalendarForms
from .models import *
from Calendar.serializers import EventSerializer
from rest_framework import viewsets
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
import json

class EventsListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
def eventcontext(request):
    events = []
    profile = Profile.objects.get(user=request.user)
    calendar = Calendar.objects.filter(user = profile)
    for event in calendar:
        events.append(Event.objects.filter(master_event = event))
    lessons = []
    for event in events:
        for lesson in event:
            lessons.append(
                {
                    'title' : f"{str(lesson.__dict__['title'])} {str(datetime.strftime(lesson.__dict__['start'],'%H:%M'))}",
                    'start' : datetime.strftime(lesson.__dict__['start'],'%Y-%m-%d'),
                    'end': datetime.strftime(lesson.__dict__['end'],'%Y-%m-%d'),
                    'url': '/home/event/' + str(lesson.__dict__['id'])
                    
                }
            )
    return lessons
    
def home(request):
    lessons = eventcontext(request)
    context = {
     'title' : 'Home',
     'lessons' : lessons,
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
            addeventfromcalendar(calendar,calendar.time_start, calendar.title) #Создаются повторяющиеся события(уроки) сроком на 1 год
        else:
            Event.objects.create(start=calendar.time_start,
                                 end = calendar.time_start,
                                 title = str(calendar.title).split(' ')[0],
                                 master_event=calendar,) #Если не повторяется создается 1 событие

        return HttpResponseRedirect(reverse('calendar:addevent'))

    def get(self,request,*args, **kwargs):
        form = AddCalendarForms
        lessons = eventcontext(request)
        students = Customer.objects.filter(user = request.user)
        context = {
        'title' : 'Home',
        'lessons' : lessons,
        'students': students,
        'form': form,
            }
        return render(request, 'calendar/addevent.html',context)

def addeventfromcalendar(calendar, time, title):
    title = str(title).split(' ')[0]
    time = datetime.strptime(time,'%Y-%m-%dT%H:%M')
    print(type(time))
    for i in range(52):
        Event.objects.create(start=time,master_event=calendar,end=time, title=title)
        time += timedelta(7)

def event(request,pk):
    event = Event.objects.get(pk=pk)
    context = {
        'title' : event.title,
        'event' : event,
    }
    return render(request, 'calendar/event.html',context)
        

