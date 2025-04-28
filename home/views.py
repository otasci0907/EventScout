# from django.http import HttpResponse
from django.shortcuts import render
from createEvents.models import Event
from .forms import DistanceFilterForm
import math


def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on earth in miles"""
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 0.621371
    return distance

def index(request):
    events = Event.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True).order_by('-start_time')
    form = DistanceFilterForm(request.GET or None)

    if form.is_valid():
        distance = int(form.cleaned_data['distance'])
        user_lat = form.cleaned_data.get('user_lat')
        user_lng = form.cleaned_data.get('user_lng')

        if user_lat and user_lng:
            filtered_events = []
            for event in events:
                if event.latitude is None or event.longitude is None:
                    continue

                event_distance = haversine(
                    float(user_lat),
                    float(user_lng),
                    float(event.latitude),
                    float(event.longitude)
                )
                if event_distance <= distance:
                    event.distance = round(event_distance, 1)
                    filtered_events.append(event)

            events = sorted(filtered_events, key=lambda x: x.distance)

    return render(request, 'home/index.html', {
        'events': events,
        'form': form,
    })