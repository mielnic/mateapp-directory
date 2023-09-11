from django import forms
from .models import Post, File
from directory.models import Person, Company
from django.utils.translation import gettext_lazy as _

class PostCreationForm(forms.ModelForm):  
    class Meta:
        model = Post 
        fields = [
            'post',
            'person',
            'company',
        ]

        widgets = {
            'post': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
            'person' : forms.Select(attrs={'class':'form-select'}),
            'company' : forms.Select(attrs={'class':'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(deleted=False).order_by('companyName')
        self.fields['company'].empty_label = _("Select Company:")
        self.fields['person'].queryset = Person.objects.filter(deleted=False).order_by('lastName')
        self.fields['person'].empty_label = _("Select Person:")

class PostEditForm(forms.ModelForm):
     '''Short form for partial edit with htmx'''

     class Meta:
        model = Post
        fields = {
            'post',
        }

        widgets = {
            'post': forms.Textarea(attrs={'class':'form-control','placeholder':'Notes','style':'height: 200px'}),
        }


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'file',
        ]

        widgets = {
            'file': forms.ClearableFileInput(attrs={'class':'form-control', 'type':'file', 'multiple' : ''})
        }


