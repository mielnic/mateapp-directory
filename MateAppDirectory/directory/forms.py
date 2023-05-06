from django import forms
from .models import Person, Company, Address


# class PersonForm(forms.Form):
#     firstName = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}), required=False)
#     lastName = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)  
#     celphone = forms.CharField(label='Cell Phone', max_length=25, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
#     workphone = forms.CharField(label='Work Phone', max_length=25, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Work Phone'}), required=False)
#     email = forms.CharField(label='eMail', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'eMail','type':'email'}), required=False)
#     company = forms.ModelChoiceField(label='Company', queryset=Company.objects.filter(deleted=False), widget=forms.Select(attrs={'class':'form-select'}), empty_label='Select Company:', required=False)
#     # address = forms.ModelChoiceField(label='Address', queryset=Address.objects.values_list('street', flat=True), required=False)
#     notes = forms.CharField(label='Notes', max_length=50, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Notes'}), required=False)
    


#     # .values_list('companyName', flat=True)to_field_name='companyName',

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = [
            'firstName',
            'lastName',
            'celphone',
            'workphone',
            'email',
            'company',
            'notes',
        ]

        widgets = {
            'firstName': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'lastName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'celphone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cell Phone'}),
            'workphone': forms.TextInput(attrs={'class':'form-control','placeholder':'Work Phone'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'eMail','type':'email'}),
            'company': forms.Select(attrs={'class':'form-select'}),
            'notes': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(deleted=False).order_by('companyName')
        self.fields['company'].empty_label = 'Select Company:'

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'companyName',
            'tax_id',
            'website',
            'companyPhone',
            'address',
        ]

        widgets = {
            'companyName': forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name'}),
            'tax_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Tax ID'}),
            'website': forms.TextInput(attrs={'class':'form-control','placeholder':'Website'}),
            'companyPhone': forms.TextInput(attrs={'class':'form-control','placeholder':'Company Phone'}),
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