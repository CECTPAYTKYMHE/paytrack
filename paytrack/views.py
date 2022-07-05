from django.shortcuts import render

def index(request):
    events  = [{
          'title' : 'All Day Event',
          'start': '2022-07-05'
        },]
    context = {
        'title' : 'Главная',
        'events' : events,
        }

    return render(request, 'main/index.html', context)