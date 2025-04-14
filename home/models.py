from django.db import models

# Create your models here.
class AttendeeUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='default@example.com')
    password = models.CharField(max_length=255)
    pfp = models.ImageField(upload_to='profile_pics/')
    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + '-' + self.last_name


class OrganizerUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='default@example.com')
    password = models.CharField(max_length=255)
    pfp = models.ImageField(upload_to='profile_pics/')
    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + '-' + self.last_name
