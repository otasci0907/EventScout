from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.set_new_password_view, name='accounts.set_new_password'),
]