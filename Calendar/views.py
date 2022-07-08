from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from Calendar.forms import AddEventForms
from .models import *
from Calendar.serializers import CalendarSerializer
from rest_framework import viewsets
from django.views import View

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

def home(request):
    events = [
        {
            'title' : 'Костя',
            'start' : '2022-07-06',
            'end': '2022-07-07',
            'url': '/',
            
        }
    ]
    context = {
     'title' : 'Home',
     'events' : events,
        }
    return render(request, 'calendar/home.html', context)

class Addevent(View):
    def post(self,request,*args, **kwargs):
        print(request.POST)
        return HttpResponseRedirect(reverse('calendar:addevent'))
        
    def get(self,request,*args, **kwargs):
        form = AddEventForms
        events = [
            {
                'title' : 'Костя',
                'start' : '2022-07-06',
                'end': '2022-07-07',
                'url': '/',
                
            }
        ]
        students = Customer.objects.filter(user = request.user)
        context = {
        'title' : 'Home',
        'events' : events,
        'students': students,
        'form': form,
            }
        return render(request, 'calendar/addevent.html',context)