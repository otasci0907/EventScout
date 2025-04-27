from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, RSVPForm
from django.contrib.auth.decorators import login_required
from .models import Event
# imports near the top
import json, os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt   # use if you don't include CSRF token
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@require_POST
def chatgpt(request):
    """Return an OpenAI answer to the posted question (+ optional context)."""
    try:
        payload = json.loads(request.body)
        question = payload["question"]
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest("Malformed JSON")

    context = []
    if title := payload.get("title"):
        context.append(f"Event title: {title}")
    if descr := payload.get("descr"):
        context.append(f"Description: {descr}")

    messages = [
        {"role": "system",
         "content": ("You are an event-planning assistant. "
                     "Give concise, actionable suggestions.")},
        {"role": "user",
         "content": "\n".join(context + [question])}
    ]

    try:
        resp = client.chat.completions.create(model="gpt-4o-mini",
        messages=messages,
        max_tokens=256,
        temperature=0.7)
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"answer": answer})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form = EventForm()
            return redirect('createEvents/create_event.html')
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
            return redirect('events.event_detail', event_id=event.id)
    else:
        form = RSVPForm()

    return render(request, 'createEvents/event_detail.html', {
        'event': event,
        'form': form,
        'rsvps': event.rsvps.all()
    })
rsvp_form = event_detail