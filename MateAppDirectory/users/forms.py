from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import Widget, TextInput, PasswordInput
from django.contrib.auth import login as auth_login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
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
            ]

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
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

class ChangePasswordForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
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
        label="email",
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}),
    )


