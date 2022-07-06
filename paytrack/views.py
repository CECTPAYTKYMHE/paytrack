from django.shortcuts import render

def login(request):
    context = {
        'title' : 'Login page',
        }

    return render(request, 'main/login.html', context)