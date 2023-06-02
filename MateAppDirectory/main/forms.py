from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control me-2', 'placeholder':'search', 'type':'search', 'aria-label':'search'}),
    )