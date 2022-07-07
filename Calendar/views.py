from django.shortcuts import render
from .models import *
from Calendar.serializers import CalendarSerializer
from rest_framework import viewsets

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