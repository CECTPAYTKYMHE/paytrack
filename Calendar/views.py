from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from Calendar.forms import AddCalendarForms, PaidEventForms
from .models import *
from Calendar.serializers import EventSerializer
from rest_framework import viewsets
from django.views import View
from django.contrib.auth.decorators import login_required
from .utils import calculate_proceeds_for_get, create_event_context, add_calendar_and_event, event_edit, calculate_proceeds_for_post


class EventsListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@login_required
def home(request):
    json_lessons = create_event_context(request)
    context = {
     'title' : 'Календарь',
     'lessons' : json_lessons,
        }
    return render(request, 'calendar/home.html', context)


class AddCalendar(View):
    """View с добавлнием события календаря, так же в ней создаются ученики если они не существовали
    и создаются события ивентов(уроков)"""

    def post(self,request,*args, **kwargs):
        add_calendar_and_event(request)
        return HttpResponseRedirect(reverse('calendar:addevent'))
    
    def get(self,request,*args, **kwargs):
        form = AddCalendarForms
        lessons = create_event_context(request)
        students = Customer.objects.filter(user = request.user)
        context = {
        'title' : 'Создание занятий',
        'lessons' : lessons,
        'students': students,
        'form': form,
            }
        return render(request, 'calendar/addevent.html',context)


class ShowEvent(View):
    """Показ и изменение события(урока) с чекбоксами о оплате и удаления события, заметки о учениках"""

    def get(self,request,pk,*args, **kwargs):
        event = Event.objects.get(pk=pk,user=request.user)
        student = Customer.objects.get(name=event.title,user=request.user)
        form = PaidEventForms()
        if event.paid:
            form.fields['paid'].widget.attrs['checked'] = ''
        context = {
                'form': form,
                'title' : event.title,
                'event' : event,
                'student_desc': student.description,
            }
        return render(request, 'calendar/event.html',context)
    
    def post(self,request,pk,*args, **kwargs):
        event_edit(request,pk)
        return redirect('calendar:home')


class Proceeds(View):
    """Калькуляция заработка"""
    def get(self,request,*args, **kwargs):
        context = calculate_proceeds_for_get(request)
        return render(request,'calendar/proceeds.html',context)
        
    def post(self,request,*args, **kwargs):
        context = calculate_proceeds_for_post(request)
        return render(request,'calendar/proceeds.html', context)
