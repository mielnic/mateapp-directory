from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('list/', views.posts_list, name='list'),
    path('view/<int:id>/', views.post_view, name='view'),
    path('post_title/<int:id>/', views.post_title, name='title'),
    path('post_post/<int:id>/', views.post_post, name='post'),
    path('post_edit/<int:id>/', views.post_edit, name='edit'),
    path('post_action/<int:id>/', views.post_action, name='action'),
    path('post_delete/<int:id>/', views.post_delete, name='delete'),
    path('post_restore/<int:id>/', views.post_restore, name='restore'),
    path('post_full_delete/<int:id>/', views.post_restore, name='full_delete'),
    # path('edit/', views.***, name='edit'),
]