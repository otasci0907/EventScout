from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db import models
USER_TYPE_CHOICES = [
    ('organizer', 'Organizer'),
    ('attendee', 'Attendee'),
]
# Create your models here.
class User(AbstractUser):
    pfp = models.ImageField(upload_to='profile_pics/')
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='organizer')
    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + '-' + self.last_name


