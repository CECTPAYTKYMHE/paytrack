from django.urls import path, include
from .views import home, Addevent

urlpatterns = [
    path('', home, name = 'home'),
    path('addevent/', Addevent.as_view(), name='addevent'),
]