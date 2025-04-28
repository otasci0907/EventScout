import logging
from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.CharField(max_length=255)
    org_email = models.EmailField(max_length=255, default="a@a.com")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.location and (not self.latitude or not self.longitude):
            try:
                geolocator = Nominatim(user_agent="eventscout")
                location = geolocator.geocode(self.location)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except Exception as e:
                logging.warning(f"Geocoding failed for {self.location}: {str(e)}")
        super().save(*args, **kwargs)
        
genderChoices = [
    ('male', 'Male'),
    ('female', 'Male'),
    ('other', 'Other'),
    ('do not wish to specify', 'Do not wish to specify')

]

class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=100, choices = genderChoices, default = 'other')
    age = models.IntegerField(default = 18)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} for {self.event.title}"
    