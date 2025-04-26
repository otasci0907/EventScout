from django import forms

class DistanceFilterForm(forms.Form):
    DISTANCE_CHOICES = [
        (5, '5 miles'),
        (10, '10 miles'),
        (25, '25 miles'),
        (50, '50 miles'),
    ]

    distance = forms.ChoiceField(
        choices=DISTANCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'distanceFilter',
            'onchange': 'this.form.submit()'
        }),
        initial=10
    )
    user_lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    user_lng = forms.FloatField(widget=forms.HiddenInput(), required=False)