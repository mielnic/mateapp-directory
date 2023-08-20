from django import forms
from .models import Person, Company, Address
from django.utils.translation import gettext_lazy as _

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = [
            'firstName',
            'lastName',
            'position',
            'celphone',
            'workphone',
            'email',
            'company',
            'notes',
        ]

        widgets = {
            'firstName': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lastName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'position': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Position'}),
            'celphone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cell Phone'}),
            'workphone': forms.TextInput(attrs={'class':'form-control','placeholder':'Work Phone'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'eMail','type':'email'}),
            'company': forms.Select(attrs={'class':'form-select'}),
            'notes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(deleted=False).order_by('companyName')
        self.fields['company'].empty_label = _("Select Company:")

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'companyName',
            'tax_id',
            'website',
            'companyPhone',
            'address',
            'companyNotes',
        ]

        widgets = {
            'companyName': forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}),
            'tax_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Tax ID'}),
            'website': forms.TextInput(attrs={'class':'form-control','placeholder':'Website'}),
            'companyPhone': forms.TextInput(attrs={'class':'form-control','placeholder':'Company Phone'}),
            'companyNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Company Notes','style':'height: 200px'}),
        }

class AddressFrom(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            'street',
            'postalCode',
            'city',
            'state',
            'country',
        ]

        widgets = {
            'street': forms.TextInput(attrs={'class':'form-control','placeholder':'Street'}),
            'postalCode': forms.TextInput(attrs={'class':'form-control','placeholder':'Postal Code'}),
            'city': forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),
            'state': forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),
            'country': forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),
        }

class PersonNotesForm(forms.ModelForm):
    '''Short form for partial edit with htmx'''

    class Meta:
        model = Person
        fields = {
            'notes',
        }

        widgets = {
            'notes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
        }

class CompanyNotesForm(forms.ModelForm):
    '''Short form for partial edit with htmx'''

    class Meta:
        model = Company
        fields = {
            'companyNotes',
        }

        widgets = {
            'companyNotes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
        }