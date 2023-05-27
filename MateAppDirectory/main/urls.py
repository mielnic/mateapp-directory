from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='Logout'),
]
