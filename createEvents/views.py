from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, RSVPForm
from django.contrib.auth.decorators import login_required
from .models import Event
from .factory import EventFactory
from django.http import JsonResponse
import os

import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
import os

# imports near the top
import json, os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt   # use if you don't include CSRF token
from openai import OpenAI
from django.http import JsonResponse
from .models import Event, RSVP
from django.shortcuts import get_object_or_404

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
from .models import Event

from collections import Counter
from .models import Event

def dashboard_view(request):
    events = Event.objects.prefetch_related('rsvps').all()

    event_gender_data = {}

    for event in events:
        genders = Counter(rsvp.gender for rsvp in event.rsvps.all())
        event_gender_data[event.id] = genders

    return render(request, 'your_template.html', {
        'your_events': events,
        'event_gender_data': event_gender_data,
    })

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
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form = EventForm()
            return redirect('events.create_event') 

    else:
        form = EventForm()

    user_events = Event.objects.filter(organizer=request.user).order_by('-start_time')

    # 🚀 Build gender counts
    event_gender_data = {}

    for event in user_events:
        gender_counts = Counter(rsvp.gender for rsvp in event.rsvps.all())
        event_gender_data[event.id] = {
            'male': gender_counts.get('male', 0),
            'female': gender_counts.get('female', 0),
            'other': gender_counts.get('other', 0),
            'do not wish to specify': gender_counts.get('do not wish to specify', 0),
        }
        

    user_events = Event.objects.filter(organizer=request.user).order_by('-start_time')

    event_gender_data = {}
    event_age_data = {}

    for event in user_events:
        # GENDER counts
        gender_counts = Counter(rsvp.gender for rsvp in event.rsvps.all())
        event_gender_data[event.id] = {
            'male': gender_counts.get('male', 0),
            'female': gender_counts.get('female', 0),
            'other': gender_counts.get('other', 0),
            'do not wish to specify': gender_counts.get('do not wish to specify', 0),
        }

        # AGE counts
        age_classes = {
            'under 18': 0,
            '18-24': 0,
            '25-34': 0,
            '35-44': 0,
            '45-54': 0,
            '55+': 0,
        }
        for rsvp in event.rsvps.all():
            if rsvp.age < 18:
                age_classes['under 18'] += 1
            elif 18 <= rsvp.age <= 24:
                age_classes['18-24'] += 1
            elif 25 <= rsvp.age <= 34:
                age_classes['25-34'] += 1
            elif 35 <= rsvp.age <= 44:
                age_classes['35-44'] += 1
            elif 45 <= rsvp.age <= 54:
                age_classes['45-54'] += 1
            else:
                age_classes['55+'] += 1

        event_age_data[event.id] = age_classes

    return render(request, 'createEvents/create_event.html', {
        'form': form,
        'your_events': user_events,
        'event_gender_data': event_gender_data,
        'event_age_data': event_age_data,   # 🚨 pass new age data
    })

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
            return redirect('events.event_detail', event_id=event.id)
    else:
        form = RSVPForm()


    return render(request, 'createEvents/event_detail.html', {
        'event': event,
        'form': form,
        'rsvps': event.rsvps.all()
    })
rsvp_form = event_detail

def getBasePrompt():
    events = Event.objects.all()
    prompt = "Today's date is " + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\n"
    prompt += "Here are the descriptions of all the events:\n\n"
    for event in Event.objects.all():
        prompt += "Title of event: " + event.title
        prompt += "\n"
        prompt += "Event Description: " + event.description + "\n"
        prompt += "Event Location: " + event.location + "\n"
        prompt += "Start and end: " + str(event.start_time) + " " + str(event.end_time) + "\n"
        prompt += "\n\n"
    return prompt
def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')

        if not user_message or len(user_message) == 0:
            return JsonResponse({'response': 'No message provided.'})
        basePrompt = getBasePrompt()
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for recommending local events."},
            {"role": "user", "content": basePrompt + user_message}
        ],
        max_tokens=500,
        temperature=0.7)

        gpt_text = response.choices[0].message.content

        return JsonResponse({'response': gpt_text})

    return JsonResponse({'error': 'Gotta be a POST request my boi.'}, status=400)
print(getBasePrompt())
def event_rsvp_data(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    rsvps = event.rsvps.all()

    # Gender counts
    gender_counts = {}
    for gender_label, _ in RSVP._meta.get_field('gender').choices:
        gender_counts[gender_label] = 0
    for rsvp in rsvps:
        gender_counts[rsvp.gender] += 1

    attendees = [
        {
            "first_name": rsvp.first_name,
            "last_name": rsvp.last_name,
            "email": rsvp.email,
            "gender": rsvp.gender,
            "age": rsvp.age
        }
        for rsvp in rsvps
    ]

    return JsonResponse({
        "genders": gender_counts,
        "attendees": attendees,
    })
