from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .models import Event

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form = EventForm()
            return redirect('create_event')
    else:
        form = EventForm()
    user_events = Event.objects.filter(organizer=request.user).order_by('-start_time')
    print(user_events)
    return render(request, 'createEvents/create_event.html', {'form': form, 'your_events': user_events})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
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
        return redirect('create_event')
    event.delete()
    return redirect('create_event')