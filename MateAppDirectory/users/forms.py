from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import Widget, TextInput, PasswordInput
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_active",
            "is_staff",
            ]

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'is_staff' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_active' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            ]
        
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
        }

class CustomUserEditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            ]
        
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'is_staff' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_active' : forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class ChangePasswordForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )

    class Meta:
        model = CustomUser
        fields = [
            'password1',
            'password2',
        ]

class PasswordResetForm(forms.Form):

    email = forms.EmailField(
        label=_("eMail"),
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}),
    )


