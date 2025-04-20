from django import forms
from .models import Event, RSVP

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Jazz Night at Central Park'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Write a detailed description of your event...'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. 123 Main St, New York, NY'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'placeholder': 'MM/DD/YYYY HH:MM',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'placeholder': 'MM/DD/YYYY HH:MM',
                'type': 'datetime-local'
            }),
        }

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }