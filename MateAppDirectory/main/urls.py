from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.search, name = 'search'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='Logout'),
    path('user_trash/<int:a>/<int:b>/', views.user_trash, name='User_Trash'),
    path('admin_trash/<int:a>/<int:b>/', views.admin_trash, name='Admin_Trash'),
]
