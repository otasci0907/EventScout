from django.contrib import admin
from .models import Event, RSVP
from django.contrib import admin
from .models import Event, RSVP

admin.site.register(RSVP)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'latitude', 'longitude', 'start_time')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'organizer')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time')
        }),
    )
