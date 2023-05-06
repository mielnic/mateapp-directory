from .models import Company, Address
from rest_framework import viewsets, permissions
from .serializers import CompanySerializer, AddressSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(deleted=False)
    serializer_class = CompanySerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.filter(deleted=False)
    serializer_class = AddressSerializer