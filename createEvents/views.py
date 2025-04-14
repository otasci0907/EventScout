from django.shortcuts import render, get_object_or_404, redirect
from .forms import EventForm, RSVPForm
from .models import Event

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventForm()
    return render(request, 'createEvents/create_event.html', {'form': form})


def event_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'createEvents/event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = RSVPForm()

    return render(request, 'createEvents/event_detail.html', {
        'event': event,
        'form': form,
        'rsvps': event.rsvps.all()
    })