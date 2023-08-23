from django.urls import path, include
from .api import CompanyViewSet, AddressViewSet, PersonViewSet
from . import views
from rest_framework import routers

app_name = 'directory'

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, 'companies')
router.register(r'address', AddressViewSet, 'address')
router.register(r'persons', PersonViewSet, 'persons')

urlpatterns = [
    path('', views.index, name='Index'),
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
    path('person_notes/<int:id>/', views.personNotes, name='personNotes'),
    path('edit_person_notes/<int:id>/', views.personNotesEdit, name='personNotesEdit'),
    path('company_notes/<int:id>/', views.companyNotes, name='companyNotes'),
    path('edit_company_notes/<int:id>/', views.companyNotesEdit, name='companyNotesEdit'),
    #  CUD Company
    path('create_company/', views.create_company, name='Create Company'),
    path('edit_company/<int:id>/', views.edit_company, name='Edit Company'),
    path('delete_company/<int:id>/', views.delete_company, name='Delete Company'),
    path('restore_company/<int:id>/<int:u>/', views.restore_company, name='Restore Company'),
    path('full_delete_company/<int:id>/', views.full_delete_company, name='Full Delete Company'),
    # Favorites
    path('link_fav/<str:obj>/<int:oid>/', views.link_favorite, name='LinkFav'),
    path('unlink_fav/<int:lid>/', views.unlink_favorite, name='UnLinkFav'),
    path('favs/', views.favs, name='Favs'),
    path('unlink_fav_favs/<int:lid>/', views.unlink_favorite_favs, name='UnLinkFavFavs'),
    #  API
    path('api/', include(router.urls))
]