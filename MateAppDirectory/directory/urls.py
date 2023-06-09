from django.urls import path, include
from .api import CompanyViewSet, AddressViewSet
from . import views
from rest_framework import routers

app_name = 'directory'

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, 'companies')
router.register(r'address', AddressViewSet, 'address')

urlpatterns = [
    path('', views.index, name='Index'),
    # path('login/', views.login, name='login'),
    # path('signout/', views.signout, name='Logout'),
    # List
    path('persons/<int:a>/<int:b>/', views.persons, name='Persons'),
    path('companies/<int:a>/<int:b>/', views.companies, name='Companies'),
    path('person/<int:id>/', views.person, name='Person'),
    path('company/<int:id>/<int:a>/<int:b>/', views.company, name='Company'),
    # CUD Person
    path('create_person/', views.create_person, name='Create Person'),
    path('edit_person/<int:id>/', views.edit_person, name='Edit Person'),
    path('delete_person/<int:id>/', views.delete_person, name='Delete Person'),
    path('restore_person/<int:id>/<int:u>/', views.restore_person, name='Restore Person'),
    path('full_delete_person/<int:id>/', views.full_delete_person, name='Full Delete Person'),
    #  CUD Company
    path('create_company/', views.create_company, name='Create Company'),
    path('edit_company/<int:id>/', views.edit_company, name='Edit Company'),
    path('delete_company/<int:id>/', views.delete_company, name='Delete Company'),
    path('restore_company/<int:id>/<int:u>/', views.restore_company, name='Restore Company'),
    path('full_delete_company/<int:id>/', views.full_delete_company, name='Full Delete Company'),
    #  API
    path('api/', include(router.urls))
]