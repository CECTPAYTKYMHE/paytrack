from django.urls import path, include
from .views import home, AddCalendar,event

urlpatterns = [
    path('', home, name = 'home'),
    path('addevent/', AddCalendar.as_view(), name='addevent'),
    path('event/<int:pk>',event, name='event'),
]