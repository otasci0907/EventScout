from .models import Event
from django.contrib.auth.models import User

class EventFactory:
    def createRegularEvent(self, organizer, email, title, description, start_time, end_time, location, lat, long):
        return Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
            org_email=email,
            latitude=lat,
            longitude=long
        )

    def createPoliticalRally(self, organizer, email, title, description, start_time, end_time, location, lat, long):
        special_description = "⚠️ POLITICAL RALLY NOTICE: THE VIEWS EXPRESSED ARE NOT IN ANY WAY ASSOCIATED WITH EVENTSCOUT\n\n" + description
        return Event(
            title=title,
            description=special_description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
            org_email=email,
            latitude=lat,
            longitude=long
        )

    def createAgeLimitEvent(self, organizer, email, title, description, start_time, end_time, location, lat, long):
        special_description = "🔒 NOTICE: EVENT IS RESTRICTED BY AGE. PLEASE CAREFULLY READ EVENT DESCRIPTION TO SEE RESTRICTIONS!\n\n" + description
        return Event(
            title=title,
            description=special_description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
            org_email=email,
            latitude=lat,
            longitude=long
        )