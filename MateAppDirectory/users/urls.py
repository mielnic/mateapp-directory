from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name = 'Register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]