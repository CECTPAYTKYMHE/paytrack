from django.urls import path, include
from .views import home, AddCalendar, ShowEvent, Proceeds
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home, name = 'home'),
    path('addevent/', login_required(AddCalendar.as_view()), name='addevent'),
    path('event/<int:pk>', login_required(ShowEvent.as_view()), name='event'),
    path('proceeds/', login_required(Proceeds.as_view()), name='proceeds'),
]