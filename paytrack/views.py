from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth, messages
from django.views import View
from paytrack.forms import ProfileForms, UserForms, UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from Calendar.models import Customer, Profile

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
        user = User.objects.get(username=request.user)
        user_form = UserForms()
        profile_form = ProfileForms()
        user_form.fields['username'].widget.attrs['value'] = user.username
        user_form.fields['email'].widget.attrs['value'] = user.email
        profile_form.fields['telegram_id'].widget.attrs['value'] = user.profile.telegram_id
        students = Customer.objects.filter(user=user)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'students': students,
        }
        return render(request,'main/account.html', context)
    
    def post(self,request,*args, **kwargs):
        Profile.objects.filter(user=request.user).update(telegram_id=int(request.POST['telegram_id']))
        # profile.update(telegram_id=int(request.POST['telegram_id']))
        return HttpResponseRedirect(reverse('myaccount'))
    
def show_student(request,pk):
    student = Customer.objects.get(pk=pk)
    context = {
        'student' : student,
    }
    return render(request,'main/students.html',context)