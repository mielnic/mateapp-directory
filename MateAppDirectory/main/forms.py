from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control q', 'placeholder':_('Search:'), 'type':'search', 'aria-label':'search', 'aria-describedby' : 'button-addon'}),
    )