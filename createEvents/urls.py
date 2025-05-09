from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name='events.create_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('', views.event_list, name='event_list'),
    path('delete/<int:event_id>/', views.delete_event, name='events.delete_event'),
    path('detail/<int:event_id>/', views.event_detail, name='events.event_detail'),
    path('rsvp/<int:event_id>/', views.rsvp_form, name='rsvp_form'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path("chatgpt/", views.chatgpt, name="events.chatgpt"),
    path("events/<int:event_id>/rsvps/", views.event_rsvp_data, name="events.rsvps"),
    path('my-rsvps/', views.my_rsvps, name='events.my_rsvps'),

]