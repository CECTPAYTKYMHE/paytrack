from django.urls import path, include
from .views import home, AddCalendar, ShowEvent, proceeds

urlpatterns = [
    path('', home, name = 'home'),
    path('addevent/', AddCalendar.as_view(), name='addevent'),
    path('event/<int:pk>', ShowEvent.as_view(), name='event'),
    path('proceeds/', proceeds, name='proceeds'),
]