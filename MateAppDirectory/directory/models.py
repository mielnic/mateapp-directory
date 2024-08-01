from django.db import models
from django.conf import settings
from datetime import date

class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)
    
    class Meta:
        abstract = True

class Address(BaseModel):
    street = models.CharField(max_length=200, blank=True)
    postalCode = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.street}, {self.city}'

class Company(BaseModel):
    companyName = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=15, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True)
    companyPhone = models.CharField(max_length=25, blank=True)
    companyNotes = models.TextField(max_length=2000, blank=True)
    companyNotes_title = models.CharField(max_length=200, blank=True, null=True)

    def title(self):
        fline = self.companyNotes.split('\n', 1)[0]
        if len(fline) > 25:
            fline = fline[:25]
            title = f'{fline}...'
        else:
            title = fline
        return title

    def save(self, *args, **kwargs):
        self.companyNotes_title = self.title()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.companyName


class Person(BaseModel):
    lastName = models.CharField(max_length=50, blank=True)
    firstName = models.CharField(max_length=50, blank=True)
    celphone = models.CharField(max_length=25, blank=True)
    workphone = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    notes = models.TextField(max_length=2000, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    notes_title = models.CharField(max_length=200, blank=True, null=True)

    def title(self):
        fline = self.notes.split('\n', 1)[0]
        if len(fline) > 25:
            fline = fline[:25]
            title = f'{fline}...'
        else:
            title = fline
        return title

    def save(self, *args, **kwargs):
        self.notes_title = self.title()
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.lastName}, {self.firstName}'


class Favorite(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)

class Lead(BaseModel):
    firstName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=False)
    message = models.CharField(max_length=500, blank=True)
    messageDate = models.DateField(blank=True, null=True, default=date.today)

    def __str__(self):
        return f'{self.lastName} - {self.messageDate}'




