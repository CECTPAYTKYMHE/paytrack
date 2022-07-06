
from django.contrib import admin
from django.urls import path, include
from .views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name = 'login'),
    path('home/', include(('Calendar.urls', 'calendar'))),
]
