from django.contrib import admin
from .models import AttendeeUser
from .models import OrganizerUser

admin.site.register(AttendeeUser)
admin.site.register(OrganizerUser)

# Register your models here.
