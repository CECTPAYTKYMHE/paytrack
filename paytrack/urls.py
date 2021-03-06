from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import login, RegisterUser, MyAccount, Show_edit_student
from Calendar.views import EventsListViewSet
from rest_framework import routers
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

router = routers.SimpleRouter()
router.register(r'events', EventsListViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name = 'login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', include(('Calendar.urls', 'calendar'))),
    path('api/', include(router.urls)),
    path('myaccount/', login_required(MyAccount.as_view()),name='myaccount'),
    path('students/<int:pk>/', login_required(Show_edit_student.as_view()), name='student'),
    path('captcha/', include('captcha.urls')),
]
