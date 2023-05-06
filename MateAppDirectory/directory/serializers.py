from rest_framework import serializers
from .models import Company, Address

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
        ]
        read_only_fields = [
            'id',
            'street',
            'postalCode',
            'city',
            'state',
            'country',
        ]