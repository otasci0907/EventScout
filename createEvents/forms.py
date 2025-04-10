from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['organizer']
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