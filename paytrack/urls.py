from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import login, register
from Calendar.views import CalendarViewSet
from rest_framework import routers
from django.contrib.auth.views import LogoutView

router = routers.DefaultRouter()
router.register(r'calendar', CalendarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name = 'login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', include(('Calendar.urls', 'calendar'))),
    path('api/v1/', include(router.urls)),
]
