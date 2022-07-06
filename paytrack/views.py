from django.shortcuts import render

def index(request):
    events  = [{
          'title' : 'Светлана',
          'start': '2022-07-05',
        'url': '/index',
        },
        {
          'title' : 'Светлана',
          'start': '2022-07-10',
        'url': '/index',
        }]
    context = {
        'title' : 'Главная',
        'events' : events,
        }

    return render(request, 'main/index.html', context)