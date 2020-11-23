import os
from django.conf import settings
from django.shortcuts import render
from .models import Route, Station

def stations_view(request):
    route = request.GET.get('route')
    if route:
        route = Route.objects.get(name=route)
        stations = route.stations.all()
    else:
        stations = Station.objects.all()
    template = 'stations.html'
    context = {
        'routes': Route.objects.all(),
        'stations': stations,
        'center': route.center(),
        'route': route,
        'yandex_api_key': settings.YANDEX_API_KEY
    }
    return render(request, template, context)


