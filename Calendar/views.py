from django.shortcuts import render

def home(request):
    events = [
        {
            'title' : 'Костя',
            'start' : '2022-07-06',
            'end': '2022-07-07',
            'url': '/',
            
        }
    ]
    context = {
     'title' : 'Home',
     'events' : events,
        }
    return render(request, 'calendar/home.html', context)