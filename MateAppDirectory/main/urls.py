from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('search/', views.search, name='search'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='Logout'),
    path('user_trash/', views.user_trash, name='User_Trash'),
    path('admin_trash/', views.admin_trash, name='Admin_Trash'),
    path('admin_home/', views.admin_home, name='Admin_Home'),
    path('backup/', views.do_backup, name='Backup'),
]
