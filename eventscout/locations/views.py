from django.shortcuts import render
from django.http import HttpResponse
from ipware import get_client_ip
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
            "longitude": -118.2437
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

def locations(request):
    return render(request, 'test.html')

@csrf_exempt # only for testing, use token in production
def get_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Process the data (e.g., save to database)
        return JsonResponse({'status': 'success', 'message': 'Location data received'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})