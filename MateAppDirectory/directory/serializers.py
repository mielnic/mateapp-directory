from rest_framework import serializers
from .models import Company, Address, Person

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'companyName',
            'tax_id',
            'address',
            'website',
            'companyPhone',
            'deleted',
            )
        read_only_fields = (
            'id',
            'companyName',
            'tax_id',
            'address',
            'website',
            'companyPhone',
            'deleted',
            )

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'postalCode',
            'city',
            'state',
            'country',
            'deleted',
        ]
        read_only_fields = [
            'id',
            'street',
            'postalCode',
            'city',
            'state',
            'country',
            'deleted',
        ]

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'lastName',
            'firstName',
            'celphone',
            'workphone',
            'email',
            'position',
            'address',
            'notes',
            'company',
            'deleted',
        ]
        read_only_fields = [
            'id',
            'lastName',
            'firstName',
            'celphone',
            'workphone',
            'email',
            'position',
            'address',
            'notes',
            'company',
            'deleted',
        ]