from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import login, register
from Calendar.views import EventsListViewSet
from rest_framework import routers
from django.contrib.auth.views import LogoutView

router = routers.SimpleRouter()
router.register(r'events', EventsListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name = 'login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', include(('Calendar.urls', 'calendar'))),
    path('api/', include(router.urls)),
]
