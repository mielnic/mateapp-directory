from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True)
    postalCode = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.street}, {self.city}'

class Company(models.Model):
    companyName = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=15, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True)
    companyPhone = models.CharField(max_length=25, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.companyName


class Person(models.Model):
    lastName = models.CharField(max_length=50, blank=True)
    firstName = models.CharField(max_length=50, blank=True)
    celphone = models.CharField(max_length=25, blank=True)
    workphone = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lastName}, {self.firstName}'






