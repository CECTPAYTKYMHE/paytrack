from django.contrib import admin
from django.urls import path, include
from .views import login
from Calendar.views import CalendarViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'calendar', CalendarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name = 'login'),
    path('home/', include(('Calendar.urls', 'calendar'))),
    path('api/v1/', include(router.urls)),
]
