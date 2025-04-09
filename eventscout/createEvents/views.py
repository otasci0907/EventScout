from django.shortcuts import render
from .forms import EventForm

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EventForm()
    return render(request, 'createEvents/create_event.html', {'form': form})