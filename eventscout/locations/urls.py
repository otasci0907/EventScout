from django.urls import path
from . import views

urlpatterns = [
    path('', views.locations, name='locations'),
]