from .models import Company, Address, Person
from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, AddressSerializer, PersonSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(deleted=False)
    serializer_class = CompanySerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(deleted=False)
    serializer_class = PersonSerializer