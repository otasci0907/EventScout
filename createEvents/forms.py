from django import forms
from .models import Event, RSVP


class EventForm(forms.ModelForm):
    typesOfEvents = [
        ('regular', 'Regular Event'),
        ('political', 'Political Rally'),
        ('age_limit', 'Age-Restricted Event'),
    ]


    event_type = forms.ChoiceField(choices=typesOfEvents, required=True)
    class Meta:
        model = Event
        exclude = ['organizer', 'org_email']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Jazz Night at Central Park'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Write a detailed description of your event...',
                'style': 'width:70%;'
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
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class RSVPForm(forms.ModelForm):
    genderChoices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('do not wish to specify', 'Do not wish to specify')

    ]

    gender = forms.ChoiceField(choices=genderChoices, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Age',
        'min': 0,
        'class': 'form-control'
    }))

    class Meta:
        model = RSVP
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'age']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RSVP.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different one.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        user.email = email
        if commit:
            user.save()
        return user
