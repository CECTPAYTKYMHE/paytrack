from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth, messages
from django.views import View
from paytrack.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from Calendar.models import Profile

def login(request):
    """Функция для авторизации пользователя"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('calendar:home'))

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('calendar:home'))
        else:
            messages.warning(request, "Неправильный логин или пароль")
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Авторизация',
    }
    return render(request,'main/login.html', context)

def register(request):
    """Функция для регистрации пользователя"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if User.objects.filter(username = request.POST['username']).first():
                messages.warning(request, "Такой пользователь уже существует")
                return redirect('register')
        elif User.objects.filter(email = request.POST['email']).first():
                messages.warning(request, "Пользователь с такой почтой уже существует")
                return redirect('register')
        if form.is_valid():
                form.save()
                user = User.objects.get(username = request.POST['username'])
                Profile.objects.create(user = user, telegram_id=request.POST['telegram_id'])
                messages.success(request, 'Вы успешно зарегистрировались')
                return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Создание профиля',
    }
    return render(request, 'main/register.html', context)

class MyAccount(View):
    
    def get(self,request,*args, **kwargs):
        
        return render(request,'main/account.html')
    