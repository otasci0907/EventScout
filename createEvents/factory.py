from .models import Event
from django.contrib.auth.models import User

class EventFactory:
    def createRegularEvent(self, organizer, title, description, start_time, end_time, location):
        return Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
        )

    def createPoliticalRally(self, organizer, title, description, start_time, end_time, location):
        special_description = "⚠️ POLITICAL RALLY NOTICE: THE VIEWS EXPRESSED ARE NOT IN ANY WAY ASSOCIATED WITH EVENTSCOUT\n\n" + description
        return Event(
            title=title,
            description=special_description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
        )

    def createAgeLimitEvent(self, organizer, title, description, start_time, end_time, location):
        special_description = "🔒 NOTICE: EVENT IS RESTRICTED BY AGE. PLEASE CAREFULLY READ EVENT DESCRIPTION TO SEE RESTRICTIONS!\n\n" + description
        return Event(
            title=title,
            description=special_description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            organizer=organizer,
        )