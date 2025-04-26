from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, RSVPForm
from django.contrib.auth.decorators import login_required
from .models import Event
from .factory import EventFactory


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_type = form.cleaned_data['event_type']
            factory = EventFactory()
            event = None
            print(request.user)
            if event_type == 'regular':
                event = factory.createRegularEvent(
                    organizer=str(request.user),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                    location=form.cleaned_data['location'],
                )
            elif event_type == 'political':
                event = factory.createPoliticalRally(
                    organizer=str(request.user),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                    location=form.cleaned_data['location'],
                )
            elif event_type == 'age_limit':
                event = factory.createAgeLimitEvent(
                    organizer=str(request.user),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                    location=form.cleaned_data['location'],
                )
            if (event != None):
                event.save()
            return redirect('events.create_event')
    else:
        form = EventForm()
    user_events = Event.objects.filter(organizer=request.user).order_by('-start_time')
    print(user_events)
    return render(request, 'createEvents/create_event.html', {'form': form, 'your_events': user_events, 'editing': False})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events.create_event')
    else:
        form = EventForm(instance=event)

    user_events = Event.objects.filter(organizer=request.user).order_by('-start_time')

    return render(request, 'createEvents/create_event.html', {
        'form': form,
        'your_events': user_events,
        'editing': True,
        'edit_event_id': event.id,
    })

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if (str(event.organizer) != str(request.user)):
        print("permission erorr", event.organizer, request.user)
        #not the organizer so doesn't have permission to delete
        return redirect('events.create_event')
    event.delete()
    return redirect('events.create_event')


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

