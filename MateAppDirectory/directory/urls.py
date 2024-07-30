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
    path('persons/', views.persons, name='Persons'),
    path('companies/', views.companies, name='Companies'),
    path('person/<int:id>/', views.person, name='Person'),
    path('company/<int:id>/<int:a>/<int:b>/', views.company, name='Company'),
    # CUD Person
    path('create_person/', views.create_person, name='CreatePerson'),
    path('edit_person/<int:id>/', views.edit_person, name='EditPerson'),
    path('delete_person/<int:id>/', views.delete_person, name='DeletePerson'),
    path('restore_person/<int:id>/<int:u>/', views.restore_person, name='RestorePerson'),
    path('full_delete_person/<int:id>/', views.full_delete_person, name='FullDeletePerson'),
    path('person_notes/<int:id>/', views.personNotes, name='personNotes'),
    path('person_notes_title/<int:id>/', views.personNotesTitle, name='personNotesTitle'),
    path('edit_person_notes/<int:id>/', views.personNotesEdit, name='personNotesEdit'),
    path('create_person_post/<int:id>/', views.personPostCreate, name='personPostCreate'),
    path('person_sticky/<int:id>/<int:pid>/', views.person_sticky, name='personSticky'),
    #  CUD Company
    path('create_company/', views.create_company, name='CreateCompany'),
    path('edit_company/<int:id>/', views.edit_company, name='EditCompany'),
    path('delete_company/<int:id>/', views.delete_company, name='DeleteCompany'),
    path('restore_company/<int:id>/<int:u>/', views.restore_company, name='RestoreCompany'),
    path('full_delete_company/<int:id>/', views.full_delete_company, name='FullDeleteCompany'),
    path('company_notes/<int:id>/', views.companyNotes, name='companyNotes'),
    path('company_notes_title/<int:id>/', views.companyNotesTitle, name='companyNotesTitle'),
    path('edit_company_notes/<int:id>/', views.companyNotesEdit, name='companyNotesEdit'),
    path('company_persons_list/<int:id>/<int:a>/<int:b>/', views.companyPersons, name='companyPersons'),
    path('company_persons_collapsed/<int:id>/', views.companyPersonsCollapsed, name=('companyPersonsCollapsed')),
    path('create_company_post/<int:id>/', views.companyPostCreate, name='companyPostCreate'),
    path('company_sticky/<int:id>/<int:cid>/', views.company_sticky, name='companySticky'),
    # Favorites
    path('link_fav/<str:obj>/<int:oid>/', views.link_favorite, name='LinkFav'),
    path('unlink_fav/<int:lid>/', views.unlink_favorite, name='UnLinkFav'),
    path('favs/', views.favs, name='Favs'),
    path('unlink_fav_favs/<int:lid>/', views.unlink_favorite_favs, name='UnLinkFavFavs'),
    #  API
    path('api/', include(router.urls))
]