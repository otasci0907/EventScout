from django.shortcuts import render
from django.http import HttpResponse
from ipware import get_client_ip
import requests
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

test_events_w_locations = [
    {
        "name": "Event 1",
        "location": "Location 1",
        "date": "2023-10-01",
        "time": "10:00 AM",
        "description": "Description for Event 1",
        "coordinates": {
            "latitude": 40.7128,
            "longitude": 74.0060
        }
    },
    {
        "name": "Event 2",
        "location": "Location 2",
        "date": "2023-10-02",
        "time": "11:00 AM",
        "description": "Description for Event 2",
        "coordinates": {
            "latitude": 34.0522,
            "longitude": -84.2437
        }
    },
    {
        "name": "Event 3",
        "location": "Location 3",
        "date": "2025-4-03",
        "time": "7:00 PM",
        "description": "Description for Event 3",
        "coordinates": {
            "latitude": -100.7128,
            "longitude": -74.0060
        }
    },
    {
        "name": "Event 4",
        "location": "Location 4",
        "date": "2023-10-04",
        "time": "11:00 PM",
        "description": "Description for Event 4",
        "coordinates": {
            "latitude": -10.0522,
            "longitude": 81.2437
        }
    },
    {
        "name": "Event 5",
        "location": "Location 5",
        "date": "2025-10-04",
        "time": "11:00 PM",
        "description": "Description for Event 5",
        "coordinates": {
            "latitude": 40.0522,
            "longitude": -101.2437
        }
    },
]

@csrf_exempt
def locations(request):
    api_key = os.environ.get('GOOGLE_API_KEY')
    data = {
        'API_KEY': api_key,
    }
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        events_in_range = get_events_in_range(1.5, float(latitude), float(longitude))
        data = {
            'events': events_in_range,
        }
        print(events_in_range)
    return render(request, 'test.html', {'data': data})

def get_events_in_range(max_dist, lat, long):
    return [event for event in test_events_w_locations if event['coordinates']['latitude'] <= lat + max_dist and event['coordinates']['latitude'] >= lat - max_dist and event['coordinates']['longitude'] <= long + max_dist and event['coordinates']['longitude'] >= long - max_dist]

def get_directions(event, lat, long):
    destination_coord = str(event["coordinates"]["latitude"]) + "," + str(event["coordinates"]["longitude"])
    origin_coord = str(lat) + "," + str(long)
    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + origin_coord + "&destination=" + destination_coord +"&key=" + api_key
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for step in data['routes'][0]['legs'][0]['steps']:
            print(step['html_instructions'])
        return data
    else:
        print(None)
        return None